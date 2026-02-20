# Explore ESS Round 3 data to identify well-being module variables
# for Huppert & So (2013) flourishing indicators

library(haven)
library(dplyr)

# Load data
ess <- read_sav("/Users/lukaswallrich/Documents/Coding/ai_reproduction/data/ess/ESS3e03_7.sav")

cat("=== Dataset dimensions ===\n")
cat("Rows:", nrow(ess), "Columns:", ncol(ess), "\n\n")

# Get all variable names and labels
var_info <- tibble(
  name = names(ess),
  label = sapply(ess, function(x) {
    lbl <- attr(x, "label")
    if (is.null(lbl)) NA_character_ else lbl
  })
)

# Search for candidate variables based on keywords from the constructs
cat("=== Identifying the 10 flourishing variables ===\n\n")

constructs <- list(
  "1. Competence (accomplishment)" = "accomplish",
  "2. Emotional stability (calm/peaceful)" = "calm|peaceful",
  "3. Engagement (learning)" = "learn",
  "4. Meaning (valuable/worthwhile)" = "valuable|worthwhile",
  "5. Optimism (optimistic/future)" = "optimis",
  "6. Positive emotion (happy)" = "happy",
  "7. Positive relationships (care)" = "care about|care for",
  "8. Resilience (wrong/back to normal)" = "wrong|back to normal|long time",
  "9. Self-esteem (positive about myself)" = "positive about",
  "10. Vitality (energy)" = "energy|energe"
)

found_vars <- c()
for (nm in names(constructs)) {
  pattern <- constructs[[nm]]
  matches <- var_info %>% filter(grepl(pattern, label, ignore.case = TRUE))
  cat(sprintf("%s:\n", nm))
  if (nrow(matches) > 0) {
    for (i in seq_len(nrow(matches))) {
      cat(sprintf("  -> %s: %s\n", matches$name[i], matches$label[i]))
      found_vars <- c(found_vars, matches$name[i])
    }
  } else {
    cat("  -> NOT FOUND\n")
  }
  cat("\n")
}

# Also search for life satisfaction
cat("=== Life satisfaction ===\n")
matches <- var_info %>% filter(grepl("satisf", label, ignore.case = TRUE))
for (i in seq_len(nrow(matches))) {
  cat(sprintf("  %s: %s\n", matches$name[i], matches$label[i]))
  found_vars <- c(found_vars, matches$name[i])
}
cat("\n")

# Check weights and country
cat("=== Weights and country ===\n")
for (v in c("cntry", "dweight", "pweight")) {
  if (v %in% names(ess)) {
    cat(sprintf("  %s: %s\n", v, attr(ess[[v]], "label")))
  } else {
    cat(sprintf("  %s: NOT FOUND\n", v))
  }
}
cat("\n")

# Function to print variable details
print_var_detail <- function(data, varname) {
  if (!varname %in% names(data)) {
    cat(sprintf("Variable '%s' NOT FOUND\n\n", varname))
    return(invisible(NULL))
  }
  x <- data[[varname]]
  cat(sprintf("Variable: %s\n", varname))
  cat(sprintf("Label: %s\n", attr(x, "label")))
  val_labels <- attr(x, "labels")
  if (!is.null(val_labels)) {
    cat("Value labels:\n")
    for (j in seq_along(val_labels)) {
      cat(sprintf("  %s = %s\n", val_labels[j], names(val_labels)[j]))
    }
  } else {
    cat("No value labels (continuous variable)\n")
    cat(sprintf("Range: %s to %s\n", min(x, na.rm = TRUE), max(x, na.rm = TRUE)))
  }
  cat(sprintf("N valid: %d, N missing: %d\n", sum(!is.na(x)), sum(is.na(x))))
  cat("\n")
}

# Print detailed info for all found variables plus key ones
cat("\n=== Detailed variable information ===\n\n")
all_vars <- unique(c(found_vars, "happy", "stflife", "cntry", "dweight", "pweight"))
for (v in all_vars) {
  print_var_detail(ess, v)
}

# List unique countries
cat("\n=== Unique countries ===\n\n")
if ("cntry" %in% names(ess)) {
  countries <- sort(unique(as.character(ess$cntry)))
  cat(paste(countries, collapse = ", "), "\n")
  cat(sprintf("\nTotal: %d countries\n", length(countries)))
  
  # Also show country with value labels if available
  val_labels <- attr(ess$cntry, "labels")
  if (!is.null(val_labels)) {
    cat("\nCountry codes and labels:\n")
    for (j in seq_along(val_labels)) {
      cat(sprintf("  %s = %s\n", val_labels[j], names(val_labels)[j]))
    }
  }
}
