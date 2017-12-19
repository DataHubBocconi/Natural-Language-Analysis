parent_path <- dirname(dirname(dirname(sys.frame(1)$ofile)))
code_path <- dirname(sys.frame(1)$ofile)
data_path <- file.path(parent_path, "Data")

df <- read.table(file.path(data_path,'rawdata.csv'), sep=",")
