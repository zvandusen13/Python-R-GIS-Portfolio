install.packages("dataRetrieval")
library(dataRetrieval)
library(dplyr)
library(tidyr)
library(ggplot2)
library(lubridate)



siteNo <- "01059000"
pCode <- "00060"
start.date <- "1995-01-01"
end.date <- "2024-03-04"

AndroData <- readNWISuv(siteNumbers = siteNo,
                       parameterCd = pCode,
                       startDate = start.date,
                       endDate = end.date)

AndroData <- renameNWISColumns(AndroData)

View(AndroData)

AndroData %>% 
  summarize(mean_1995_2024 = mean(Flow_Inst, na.rm = TRUE),
            median_1995_2024 = median(Flow_Inst, na.rm = TRUE))

#Discharge Plotted from Jan 1 1995 - March 4 2024
full_discharge_plot <- ggplot(data = AndroData,
             aes(dateTime, Flow_Inst)) + geom_line() + labs(title = "Instantaneous Flow over Time", 
                                                            x = "Date (1995 - 2024)",y = "Instantenous Flow",
                                                         caption = "Data come from the USGS")

print(full_discharge_plot)

#Twenty Five Year Average Flows
start_time <- "1995-10-01 04:15:00"
end_time <- 	"2019-12-31 18:45:00"

twenty_five_year <- subset(AndroData, dateTime >= start_time & dateTime <= end_time)

twenty_five_year_average <- twenty_five_year %>%
  mutate(Month = month(dateTime),Day = day(dateTime),Time = format(dateTime, "%H:%M:%S")) %>%
  group_by(Month, Day, Time) %>%
  summarise(average_flow = mean(Flow_Inst, na.rm = TRUE)) %>%
  mutate(DateTimeID = as.POSIXct(paste("2000",Month, Day, Time, sep = "-")))

View(twenty_five_year_average)

#Annual Flow Data 2020-2023
twenty_twenty <- AndroData %>%
  filter(dateTime >= "2019-12-31 19:00:00" & dateTime <= "2020-12-31 18:45:00") %>%
  mutate(dateTime = as.POSIXct(dateTime)) %>%
  mutate(dateTime = update(dateTime, year = 2000))

twenty_twenty_one <- AndroData %>%
  filter(dateTime >= "2020-12-31 19:00:00", dateTime <= "2021-12-31 18:45:00") %>%
  mutate(dateTime = as.POSIXct(dateTime)) %>%
  mutate(dateTime = update(dateTime, year = 2000)) 

twenty_twenty_two <- AndroData %>%
  filter(dateTime >= "2021-12-31 19:00:00", dateTime <= "2022-12-31 18:45:00") %>%
  mutate(dateTime = as.POSIXct(dateTime)) %>%
  mutate(dateTime = update(dateTime, year = 2000)) 

twenty_twenty_three <- AndroData %>%
  filter(dateTime >= "2022-12-31 19:00:00", dateTime <= "2023-12-31 18:45:00") %>%
  mutate(dateTime = as.POSIXct(dateTime)) %>%
  mutate(dateTime = update(dateTime, year = 2000)) 
                              
View(twenty_twenty)
View(twenty_twenty_one)
View(twenty_twenty_two)
View(twenty_twenty_three)

#Plot Overlaying Average Annual Flow and Flows from 2020-2023
overlay_plot <- ggplot() +
  geom_line(data = twenty_five_year_average, aes(x = DateTimeID, y = average_flow, group = 1, color = "blue"), linewidth = 2) +
  geom_line(data = twenty_twenty, aes(x = dateTime, y = Flow_Inst, color = "green")) +
  geom_line(data = twenty_twenty_one, aes(x = dateTime, y = Flow_Inst, color = "red")) +
  geom_line(data = twenty_twenty_two, aes(x = dateTime, y = Flow_Inst, color = "yellow")) +
  geom_line(data = twenty_twenty_three, aes(x = dateTime, y = Flow_Inst, color = "aquamarine")) +
  scale_colour_manual(name = 'Year', 
                      values =c( 'blue'='blue',
                                 'aquamarine' = 'aquamarine',
                                 'red'= 'red','green'='green',
                                 'yellow' = 'yellow'),
                      labels = c( '2023','1995-2019','2020', '2021' ,'2022' )) +
  scale_x_datetime(date_breaks = "4 months", date_labels = "%b") +
  labs(title = "Instantaneous Flow over Time (Mean Values from 1995-2019)",
       x = "Date (1995 - 2019)",
       y = "Mean Instantaneous Flow",
       caption = "Data come from the USGS",
       color = "Series") # Note: 'color' label should match what the legend should represent

print(overlay_plot)

#Reoccurrence_Interval w/ 2023

Reoccurrence_Interval <- AndroData %>%
  filter(dateTime >= "1995-12-31 19:00:00", dateTime <= "2023-12-31 18:45:00") %>%
  mutate(Year = year(dateTime)) %>%
  group_by(Year) %>%          
  summarise(Max_Flow = max(Flow_Inst)) %>%
  arrange(desc(Max_Flow)) %>%
  mutate(Flow_Rank = rank(-Max_Flow)) %>%
  mutate(RI = (28 + 1)/Flow_Rank)

View(Reoccurrence_Interval)

reoccurrence_model <- lm(Max_Flow ~ log(RI), data = Reoccurrence_Interval)
RI_r_squared <- summary(reoccurrence_model)$r.squared

print(RI_r_squared)

model_coefficients <- coef(reoccurrence_model)
intercept <- model_coefficients[1]  # Intercept
slope <- model_coefficients[2]      # Slope of the logarithm of x

summary(model_coefficients)
equation <- sprintf("FLow_Inst = %.2f + %.2f*log(RI)", intercept, slope)
print(equation)
# "Flow_Inst = 35627.12 + 9328.25*log(RI)"
equation_final <-
  function(RI) {
    35627.12 + 9328.25*log(RI)}

# Hundred Year Flood
hundred_year_flood <- 35627.12 + (9328.25 * log(100))
print(hundred_year_flood)
# Hundred Year Flood = 78585.3

# 50 Year Flood
fifty_year_flood <- 35627.12 + 9328.25 * log(50)
print(fifty_year_flood)
# 50 Year Flood = 72119.45

# 25 Year Flood
twenty_five_year_flood <- 35627.12 + 9328.25 * log(25)
print(twenty_five_year_flood)
# 25 Year Flood = 65653.6

# 5 Year Flood
five_year_flood <- 35627.12 + 9328.25 * log(5)
print(five_year_flood)
# 5 year Flood = 50640.36

# December 2023 Event 
# 78300 =  35627.12 + 9328.25 * log(x)
# x = 96.99
# 96.99 Year Flood

reoccurrence_plot <- ggplot(Reoccurrence_Interval, aes(RI, Max_Flow)) +
  geom_point() + stat_function(fun = equation_final, geom = "line", color = "blue") +
  scale_x_continuous(trans = "log10", labels = scales::number_format()) + xlim(0,100) +
  labs(title = "Reoccurence Interval of Each Discharge Level",
     x = "Reoccurence Interval", y = "Discharge (ft^3/s)",
     caption = "Data come from the USGS")

print(reoccurrence_plot)

#Duration Curve
total_values <- 968014

Duration_Curve_data <- AndroData %>%
  mutate(Flow_Inst_Rank = rank(desc(Flow_Inst))) %>%
  arrange(Flow_Inst_Rank) %>%
  mutate(duration_value= (Flow_Inst_Rank/(1+ total_values)*100))

duration_curve_plot <- ggplot(Duration_Curve_data, aes(duration_value, Flow_Inst)) +
  geom_line() + 
  labs(title = "Duration Curve",
       x = "Percent of Time Indicated Discharge Was Met or Exceeded",
       y = "Discharge (ft^3/s)", caption = "Data come from the USGS")  +
  scale_x_continuous(trans = "log10", labels = scales::number_format()) 

print(duration_curve_plot)

#Flood Threshold Surpassing
upper_threshold <- quantile(twenty_five_year$Flow_Inst, 0.995)
print(upper_threshold)
#99.5th percentile = 39200  

flooding_events_df <- AndroData %>%
  filter(Flow_Inst > upper_threshold)

flooding_events_plot <- ggplot(flooding_events_df, aes(dateTime, Flow_Inst)) +  
  geom_point() +
  labs(title = "Flooding Events Exceeding 39200 cfs 1995 - Present ",
       x = "Date", y = "Discharge (ft^2/s)", 
       caption = "Data come from the USGS") 

print(flooding_events_plot)

