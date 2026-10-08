#!/usr/bin/env Rscript
# ==============================================================================
# Financial Plotting Engine via ggplot2
# Generates publication-quality financial charts for investment memos.
# ==============================================================================

suppressPackageStartupMessages({
  if (!require("ggplot2", quietly = TRUE)) {
    install.packages("ggplot2", repos = "https://cloud.r-project.org")
    library(ggplot2)
  }
  if (!require("jsonlite", quietly = TRUE)) {
    install.packages("jsonlite", repos = "https://cloud.r-project.org")
    library(jsonlite)
  }
})

args <- commandArgs(trailingOnly = TRUE)

if (length(args) < 2) {
  cat("Usage: Rscript financial_plots.R <input_json_path> <output_image_path>\n")
  quit(status = 1)
}

input_json <- args[1]
output_img <- args[2]

# Load and parse financial metrics payload
data <- fromJSON(input_json)

# Create high-aesthetic ggplot2 chart
# Data format expected: list with 'ticker', 'metric_name', and 'series' dataframe (year/quarter, value)
df <- as.data.frame(data$series)

p <- ggplot(df, aes(x = period, y = value, group = 1)) +
  geom_area(fill = "#3b82f6", alpha = 0.15) +
  geom_line(color = "#2563eb", linewidth = 1.2) +
  geom_point(color = "#1d4ed8", size = 3) +
  geom_text(aes(label = sprintf("$%.1fB", value)), vjust = -1, size = 3.5, fontface = "bold", color = "#1e293b") +
  labs(
    title = sprintf("%s: %s Trend", data$ticker, data$metric_name),
    subtitle = "Source: Ingested SEC Disclosures & Multi-Agent Financial Extraction",
    x = "Reporting Period",
    y = sprintf("%s", data$unit)
  ) +
  theme_minimal(base_size = 13) +
  theme(
    plot.title = element_text(face = "bold", size = 15, color = "#0f172a"),
    plot.subtitle = element_text(color = "#64748b", margin = margin(b = 15)),
    panel.grid.minor = element_blank(),
    panel.grid.major.x = element_blank(),
    panel.grid.major.y = element_line(color = "#e2e8f0", linewidth = 0.5),
    axis.title = element_text(face = "bold", color = "#475569"),
    axis.text = element_text(color = "#334155")
  )

# Save chart as high-resolution PNG
ggsave(output_img, plot = p, width = 8, height = 4.5, dpi = 300)
cat(sprintf("Successfully generated R plot at: %s\n", output_img))
