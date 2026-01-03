#The code is generated using Google Gemini on December 15, 2025
#Prompts direct the model to:

#1. Write R code to read soil data from an Excel file where EC is the dependent variable and clay (%) and organic carbon (%) are independent variables.

#2. Perform multiple linear regression with EC as the response variable and clay and organic carbon as predictors.

#3. Calculate standardized regression coefficients to assess the relative importance of the predictors.

#4. Create a data frame containing only the standardized beta coefficients of clay and organic carbon for visualization.

#5. Generate a bar plot using ggplot2 showing standardized beta coefficients with value labels and a zero reference line.

#6. Print the full regression summary and keep the script well-commented for reproducibility.

#
#Note: The code modified as per requirement of the study.






library(readxl)
library(lm.beta)
library(ggplot2)
library(dplyr) # For data manipulation (pipe operator: %>%)

# --- STEP 1: Load the Data ---

# IMPORTANT: Replace 'input_data.xlsx' with the actual path/name of your Excel file.
# We assume the data is on the first sheet (sheet = 1).
tryCatch({
  data_df <- read_excel("G:/RProgramming/V1.xlsx", sheet = 1)
  
  # Ensure the column names match exactly what you specified
  # Rename columns to simpler names for easy coding
  names(data_df)[1] <- "Y"    # EC (dS m-1)
  names(data_df)[2] <- "X1"   # Clay (%)
  names(data_df)[3] <- "X2"   # OC (%)
  
  # Check the structure of the imported data
  print("--- Data Structure ---")
  print(head(data_df))
  print(str(data_df))
  
  # Ensure variables are numeric (crucial for regression)
  data_df <- data_df %>%
    mutate(across(c(Y, X1, X2), as.numeric))
  
}, error = function(e) {
  stop(paste("Error reading Excel file:", e$message, 
             "Please ensure the file 'input_data.xlsx' exists and the sheet number is correct."))
})


# --- STEP 2: Run Multiple Linear Regression ---

# Formula: Y is predicted by X1 and X2
model <- lm(Y ~ X1 + X2, data = data_df)


# --- STEP 3: Calculate Standardized Beta Coefficients (Relative Importance Test) ---

# Use the lm.beta package to calculate the standardized coefficients
# The output provides the B (unstandardized) and Beta (standardized) values
standardized_model <- lm.beta(model)
beta_coefficients <- standardized_model$standardized.coefficients

print("--- Standardized Regression Coefficients (Beta*) ---")
print(beta_coefficients)

# --- STEP 4: Prepare Data for Plotting ---

# Create a data frame for plotting the Standardized Beta values
# We only want X1 and X2 (skip the Intercept)
plot_data <- data.frame(
  Predictor = c("Clay (%)", "OC (%)"),
  Standardized_Beta = beta_coefficients[2:3] # [2:3] selects X1 and X2 coefficients
)

# --- STEP 5: Plot the Standardized Beta Coefficients ---

# Use ggplot2 to create a bar chart for relative importance
beta_plot <- ggplot(plot_data, aes(x = Predictor, y = Standardized_Beta, fill = Predictor)) +
  geom_bar(stat = "identity", color = "black") + # stat="identity" uses the value directly
  geom_text(aes(label = sprintf("%.4f", Standardized_Beta)), # Add the beta value as text
            vjust = ifelse(plot_data$Standardized_Beta > 0, -0.5, 1.5), # Adjust label position
            color = "black", size = 5) +
  labs(
    title = "Relative Importance of Predictors (Standardized Beta)",
    x = "Predictor Variable",
    y = "Standardized Beta Coefficient (β*)"
  ) +
  theme_minimal(base_size = 14) +
  theme(legend.position = "none") +
  # Add a horizontal line at 0 for visual reference
  geom_hline(yintercept = 0, linetype = "dashed", color = "gray50")

# Display the plot
print(beta_plot)

# To save the plot:
# ggsave("Standardized_Beta_Plot.png", beta_plot, width = 7, height = 5)

# --- STEP 6: Report Full Regression Summary (Optional but Recommended) ---
print("--- Full Multiple Regression Summary ---")
summary(model)