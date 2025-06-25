using CsvHelper;
using CsvHelper.Configuration;
using System.Dynamic;
using System.Globalization;
using Microsoft.AspNetCore.Components.Forms;

namespace DataFlowInsights.Data
{
    public class FileData
    {
        public string FileId { get; set; } = string.Empty;
        public string FileName { get; set; } = string.Empty;
        public List<string> ColumnNames { get; set; } = new List<string>();
        public List<dynamic> Records { get; set; } = new List<dynamic>();
        public DateTime UploadTime { get; set; }
    }

    public class DataService
    {
        private readonly Dictionary<string, FileData> _uploadedData = new Dictionary<string, FileData>();
        private readonly long _maxFileSize = 1024 * 1024 * 20; // 20 MB limit, por ejemplo

        public async Task<(bool Success, string Message, string? FileId)> LoadCsvDataAsync(IBrowserFile file)
        {
            if (file == null)
            {
                return (false, "No se ha seleccionado ningún archivo.", null);
            }

            if (file.Size > _maxFileSize)
            {
                return (false, $"El archivo es demasiado grande. El tamaño máximo permitido es de {_maxFileSize / (1024 * 1024)} MB.", null);
            }

            try
            {
                var fileId = Guid.NewGuid().ToString();
                var fileData = new FileData { FileId = fileId, FileName = file.Name, UploadTime = DateTime.UtcNow };

                // CsvHelper necesita un Stream para leer.
                // Abrimos un stream desde IBrowserFile.
                // Usamos ReadOnlySharedStreamAsync para evitar problemas con streams grandes en Blazor Server.
                await using var stream = file.OpenReadStream(_maxFileSize);
                using var reader = new StreamReader(stream);
                using var csv = new CsvReader(reader, new CsvConfiguration(CultureInfo.InvariantCulture)
                {
                    // Opcional: Configurar CsvHelper si es necesario (ej. delimitador, cabeceras)
                    HasHeaderRecord = true,
                });

                csv.Read();
                csv.ReadHeader();
                fileData.ColumnNames = csv.HeaderRecord?.ToList() ?? new List<string>();

                fileData.Records = csv.GetRecords<dynamic>().ToList();

                if (!fileData.ColumnNames.Any() || !fileData.Records.Any())
                {
                    return (false, "El archivo CSV está vacío o no tiene cabeceras.", null);
                }

                _uploadedData[fileId] = fileData;

                return (true, "Archivo cargado y procesado exitosamente.", fileId);
            }
            catch (HeaderValidationException ex)
            {
                return (false, $"Error de validación de cabecera del CSV: {ex.Message}. Asegúrate de que el archivo CSV tenga cabeceras válidas.", null);
            }
            catch (CsvHelperException ex)
            {
                return (false, $"Error al leer el archivo CSV con CsvHelper: {ex.Message}", null);
            }
            catch (Exception ex)
            {
                // Loguear el error real en un sistema de logging en producción
                Console.WriteLine($"Error general al procesar el archivo: {ex.ToString()}");
                return (false, $"Error general al procesar el archivo: {ex.Message}", null);
            }
        }

        public FileData? GetFileData(string fileId)
        {
            _uploadedData.TryGetValue(fileId, out var fileData);
            return fileData;
        }

        public List<string>? GetColumnNames(string fileId)
        {
            if (_uploadedData.TryGetValue(fileId, out var fileData))
            {
                return fileData.ColumnNames;
            }
            return null;
        }

        public ColumnFilterInfo? GetDataForFilters(string fileId, List<string> selectedColumns)
        {
            if (!_uploadedData.TryGetValue(fileId, out var fileData) || !fileData.Records.Any())
            {
                return null;
            }

            var filterInfo = new ColumnFilterInfo();

            foreach (var columnName in selectedColumns)
            {
                if (!fileData.ColumnNames.Contains(columnName)) continue;

                var columnValues = new List<object?>();
                foreach (var record in fileData.Records)
                {
                    var expandoDict = record as IDictionary<string, object>;
                    if (expandoDict != null && expandoDict.TryGetValue(columnName, out var value))
                    {
                        columnValues.Add(value);
                    }
                    else
                    {
                        columnValues.Add(null); // Añadir null si la propiedad no existe en el objeto dinámico
                    }
                }

                // Intentar determinar el tipo de datos de la columna
                // Esto es una simplificación; una detección de tipos más robusta sería necesaria para producción.
                bool isNumeric = columnValues.All(v => v == null || double.TryParse(v?.ToString(), NumberStyles.Any, CultureInfo.InvariantCulture, out _));

                if (isNumeric)
                {
                    var numericValues = columnValues.Select(v =>
                        v == null ? (double?)null : (double.TryParse(v.ToString(), NumberStyles.Any, CultureInfo.InvariantCulture, out var num) ? num : (double?)null))
                        .Where(v => v.HasValue)
                        .Select(v => v.Value)
                        .ToList();

                    if (numericValues.Any())
                    {
                        filterInfo.NumericRanges[columnName] = new NumericRange { Min = numericValues.Min(), Max = numericValues.Max() };
                        filterInfo.SelectedNumericColumns.Add(columnName);
                    }
                    // Si todos son null o no parseables, podríamos tratarla como categórica o ignorarla.
                    // Por ahora, si no hay valores numéricos válidos, no se añade a NumericRanges.
                }
                else // Tratar como categórica si no es consistentemente numérica
                {
                    var uniqueValues = columnValues.Where(v => v != null)
                                                   .Select(v => v!) // v ya no es null aquí
                                                   .Distinct()
                                                   .ToList();
                    if (uniqueValues.Any())
                    {
                        filterInfo.CategoricalUniqueValues[columnName] = uniqueValues;
                        filterInfo.SelectedCategoricalColumns.Add(columnName);
                    }
                }
            }
            return filterInfo;
        }

        public List<dynamic>? GetFilteredData(string fileId, List<string> selectedColumns, List<AppliedFilter>? filters)
        {
            if (!_uploadedData.TryGetValue(fileId, out var fileData) || !fileData.Records.Any())
            {
                return null;
            }

            IEnumerable<dynamic> filteredRecords = fileData.Records;

            if (filters != null && filters.Any())
            {
                foreach (var filter in filters)
                {
                    if (!fileData.ColumnNames.Contains(filter.ColumnName)) continue;

                    filteredRecords = filteredRecords.Where(record =>
                    {
                        var expandoDict = record as IDictionary<string, object>;
                        if (expandoDict == null || !expandoDict.TryGetValue(filter.ColumnName, out var rawValue) || rawValue == null)
                        {
                            return false; // Si la columna no existe o el valor es null, no cumple el filtro
                        }

                        if (filter.Type == FilterType.NumericRange && filter.NumericRangeValue != null)
                        {
                            if (double.TryParse(rawValue.ToString(), NumberStyles.Any, CultureInfo.InvariantCulture, out double numericValue))
                            {
                                return numericValue >= filter.NumericRangeValue.Min && numericValue <= filter.NumericRangeValue.Max;
                            }
                            return false; // No se pudo convertir a número, no cumple
                        }
                        else if (filter.Type == FilterType.Categorical && filter.CategoricalValues != null && filter.CategoricalValues.Any())
                        {
                            // Asegurarse de que la comparación de tipos sea robusta si los valores vienen de JSON (pueden ser int64 vs int32, etc.)
                            // Convertimos ambos a string para una comparación más simple y genérica en este contexto de datos dinámicos.
                            // Para un rendimiento óptimo con tipos conocidos, se haría una conversión/comparación de tipo específico.
                            string? recordValueString = rawValue?.ToString(); // Comprobación de nulabilidad aquí
                            return filter.CategoricalValues.Any(catVal => catVal?.ToString() == recordValueString);
                        }
                        return true; // Si el filtro no es aplicable o está mal configurado, no se filtra por él
                    });
                }
            }

            // Proyectar solo las columnas seleccionadas
            var result = new List<dynamic>();
            foreach (var record in filteredRecords)
            {
                var expandoDict = record as IDictionary<string, object>;
                if (expandoDict == null) continue;

                var projectedRecord = new ExpandoObject() as IDictionary<string, object>;
                foreach (var columnName in selectedColumns)
                {
                    if (expandoDict.TryGetValue(columnName, out var value))
                    {
                        projectedRecord[columnName] = value;
                    }
                }
                if (projectedRecord.Any()) // Solo añadir si tiene alguna propiedad (evita objetos vacíos si todas las columnas seleccionadas faltaban)
                {
                    result.Add(projectedRecord);
                }
            }
            return result;
        }
    }
}
