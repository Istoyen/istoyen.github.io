// Create a blank query named ImportCsv; paste this function into Advanced Editor.
// RootPath is a text parameter pointing to the data folder. Include a trailing / or \.
(fileName as text) as table =>
let
    Source = Csv.Document(File.Contents(RootPath & fileName), [Delimiter=",", Encoding=65001, QuoteStyle=QuoteStyle.Csv]),
    Headers = Table.PromoteHeaders(Source, [PromoteAllScalars=true]),
    BlanksAsNull = Table.ReplaceValue(Headers, "", null, Replacer.ReplaceValue, Table.ColumnNames(Headers))
in
    BlanksAsNull
