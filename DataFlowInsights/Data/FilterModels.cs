namespace DataFlowInsights.Data
{
    public class ColumnFilterInfo
    {
        public Dictionary<string, NumericRange> NumericRanges { get; set; } = new Dictionary<string, NumericRange>();
        public Dictionary<string, List<object>> CategoricalUniqueValues { get; set; } = new Dictionary<string, List<object>>();
        public List<string> SelectedNumericColumns { get; set; } = new List<string>();
        public List<string> SelectedCategoricalColumns { get; set; } = new List<string>();
    }

    public class NumericRange
    {
        public double Min { get; set; }
        public double Max { get; set; }
    }

    // Modelo para representar los filtros aplicados desde el frontend
    public class AppliedFilter
    {
        public string ColumnName { get; set; } = string.Empty;
        public FilterType Type { get; set; }
        public NumericRange? NumericRangeValue { get; set; } // Usado si Type es NumericRange
        public List<object>? CategoricalValues { get; set; } // Usado si Type es Categorical
    }

    public enum FilterType
    {
        NumericRange,
        Categorical
    }
}
