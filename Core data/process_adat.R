library(SomaDataIO)

# Path to the .adat file
adat_path <- "C:/Software eng grp project basic test y3/name1/Core data/SS-2342309_v4.1_other.hybNorm.medNormInt.plateScale.adat"

# Load the .adat file
my_adat <- read_adat(adat_path)

# Check if the object is correctly loaded as a soma_adat object
is.soma_adat(my_adat)

# View the structure of the loaded data
str(my_adat)

# Optionally, convert to a data frame and save to CSV
protein_data <- as.data.frame(my_adat)
write.csv(protein_data, "C:/Software eng grp project basic test y3/name1/Core data/protein_data.csv", row.names = FALSE)
