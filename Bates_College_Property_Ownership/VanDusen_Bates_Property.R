install.packages("sf")
install.packages("ggplot2")
install.packages("tidyverse")

library(sf)
library(ggplot2)
library(osmdata)
library(tidyverse)


############# Plot of Shapefile and  #################
# Plots the shapefiles of the area surrounding Bates. The properties owned by
# Bates are shaded according to their value

#loads the Bates area shape file
parcel_shapefile <- st_read("data/LewistonParcelsBates-area.shp")
bates_parcels_csv <- read_csv("data/FinalDataset.csv") #Load .csv file we created. Contains info about the current assessed value, address,#sale data, and sale value

#initializes new column to 0
parcel_shapefile$Bates_Value = 0
#for loop parcing through each address owned by Bates
for(i in 1:nrow(bates_parcels_csv)){
  #isolates each property owned by Bates in the shape file
  property <- which(parcel_shapefile$FULL_LOCAT == bates_parcels_csv$Address[i])
  #colors each property by value of the property
  parcel_shapefile$Bates_Value[property] = bates_parcels_csv$Current_Assesed_Value[i]
}

#Uses ggplot to create overlaying plot
ggplot() +
  #plots geometric shapes from shape file
  geom_sf(data = parcel_shapefile, aes(fill = parcel_shapefile$Bates_Value), color = "black", size = 0.5)  +
  #establishes desired color scale, and makes it logarithmic to account so the very valuable properties do not skew the color cheme
  scale_fill_gradient(low = "lightblue", high = "red", trans = "log", name = "Current Assessed Value") 

############# Wilcox Test of Purchased Price vs. Current Assessors Value #################
# This is a Wilcox test of the purchased price vs the current assessors price. 
# A Wilcox test was used because the distribution is not normal. There is no
# predictable pattern in the sale price vs time. 

#eliminates the many rows with NA values
bates_buy <- na.omit(bates_parcels_csv)

#Ensures the Sale date is in the proper 'Date' format

#Changes Sale_Amount column to numeric values
bates_buy$Sale_Amount <- as.numeric(bates_buy$Sale_Amount)
#Changes Current Assesed Value column to numeric values
bates_buy$Current_Assesed_Value <- as.numeric(bates_buy$Current_Assesed_Value)

#Runs wilcox test
wilcox.test(bates_buy$Current_Assesed_Value, bates_buy$Sale_Amount)

############# Bates Property Purchasing History #################

# This plot visualizes each property bought and the purchasing price. Only a 
# fraction of the properties in the database had available purchasing information
# available

#Changes the date data to the appropriate Date format
bates_buy$Sale_Date <-as.Date(bates_buy$Sale_Date, format = "%m/%d/%Y")
print(bates_buy)

#uses appropriate data set and colums
ggplot(bates_buy, aes(x = Sale_Date, y = Sale_Amount)) + 
  geom_point(size = 3, color = "blue") +  
  #establishes x axis are dates
  scale_x_date(
    #establishes proper date format
    date_labels = "%m/%d/%Y",  
    #axis labels are every 3 years
    date_breaks = "3 year"    
  ) + 
  #labels plot
  labs(title = "Bates Property Purchasing History", x = "Date", y = "Sale Amount") 

############# Bates Property Value Change #################

# This plot visualizes the change of each of the property (with available 
# purchasing records) values. It uses the purchasing price and the current
# assessors value

#elimates outlier that was bought and is valued at millions of dollars higher than the rest
#Should be noted this datapoint declined in value as well
bates_buy <- bates_buy[bates_buy$Address != "96 CAMPUS AVE", ]

#Chooses appropriate datapoint
ggplot(bates_buy) +
  #plots line between purchasing value and current assessors value, assumes Jan 1 2024 is current assesors value
  geom_segment(aes(x = bates_buy$Sale_Date, y = bates_buy$Sale_Amount, xend = as.Date("2024-01-01") , yend = bates_buy$Current_Assesed_Value), 
               color = "blue", size = 0.25) +
  #plots sale price vs sale data
  geom_point(aes(x =  bates_buy$Sale_Date, y = bates_buy$Sale_Amount), color = "black", size = 2) +
  #plots current assessors value to Jan 1 2024
  geom_point(aes(x =  as.Date("2024-01-01"), y = bates_buy$Current_Assesed_Value), color = "black", size = 2) +
  #labels
  labs(title = "Bates Property Value Change vs. Time", x = "X-axis", y = "Y-axis") 

