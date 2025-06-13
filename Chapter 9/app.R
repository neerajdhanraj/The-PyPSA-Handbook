# ==============================================================================
# Case Study: Chapter 9 – Interactive Grid Planning with PyPSA and Shiny
#
# Authors:   Neeraj Dhanraj Bokde  (www.neerajbokde.in)
#            Carlo Fanara
# Affiliation: Renewable & Sustainable Energy Research Center, TII, Abu Dhabi
# Corresponding author: neeraj.bokde@tii.ae / neerajdhanraj@gmail.com
#
# Description:
#   This script implements the core Python backend model for the interactive
#   case study in Chapter 9 ("Integrating PyPSA with Other Tools") of
#   The PyPSA Handbook. It defines a compact power system across three Danish
#   cities—Copenhagen, Aarhus, and Aalborg—with customizable generator capacities,
#   marginal costs, and load profiles. The script enables users to evaluate
#   dispatch and power flows in real-time based on input parameters passed
#   from a Shiny app frontend.
#
#   Key Features:
#   - Three-node AC power network with user-defined generation and load
#   - Wind, solar, and gas generators at different locations
#   - Real-time linear OPF solution using PyPSA
#   - Results returned to the frontend include dispatch, line flows, and layout
#
# Book Reference:
#   Bokde, N. D., & Fanara, C. (2025). Integrating PyPSA with Other Tools.
#   In: The PyPSA Handbook: Integrated Power System Analysis and Renewable
#   Energy Modeling, Chapter 9.
#   Publisher: Elsevier Science
#   ISBN: 044326631X, 9780443266317
#
# Software Dependencies:
#   - Python 3.8+
#   - pypsa (v0.21+ recommended)
#   - pandas
#
# License: MIT
# Version: 1.0
# Date: June 2025
# ==============================================================================


library(shiny)
library(reticulate)
library(leaflet)
library(DT)

# Import the Python function from pypsa_model.py.
source_python("pypsa_model.py")



ui <- fluidPage(
  titlePanel("Regional Power Grid Optimization"),

  sidebarLayout(
    sidebarPanel(
      h4("Load Settings (MW)"),
      numericInput("demand_Copenhagen", "Copenhagen Demand (MW)", value = 50, min = 0, step = 1),
      numericInput("demand_Aarhus", "Aarhus Demand (MW)", value = 50, min = 0, step = 1),
      numericInput("demand_Aalborg", "Aalborg Demand (MW)", value = 50, min = 0, step = 1),
      hr(),
      h4("Generation Settings"),
      # Copenhagen (Wind)
      fluidRow(
        column(6,
               h5("Copenhagen (Wind)"),
               numericInput("capacity_wind", "Capacity (MW)", value = 100, min = 0, step = 1)
        ),
        column(6,
               br(),
               br(),
               numericInput("cost_wind", "Marginal Cost (€/MWh)", value = 20, min = 0, step = 1)
        )
      ),
      hr(),
      # Aarhus (Solar)
      fluidRow(
        column(6,
               h5("Aarhus (Solar)"),
               numericInput("capacity_solar", "Capacity (MW)", value = 80, min = 0, step = 1)
        ),
        column(6,
               br(),
               br(),
               numericInput("cost_solar", "Marginal Cost (€/MWh)", value = 25, min = 0, step = 1)
        )
      ),
      hr(),
      # Aalborg (Gas)
      fluidRow(
        column(6,
               h5("Aalborg (Gas)"),
               numericInput("capacity_gas", "Capacity (MW)", value = 120, min = 0, step = 1)
        ),
        column(6,
               br(),
               br(),
               numericInput("cost_gas", "Marginal Cost (€/MWh)", value = 50, min = 0, step = 1)
        )
      ),
      hr(),
      actionButton("run_model", "Run Optimization"),
      width = 4  # Increased sidebar width for side-by-side layout
    ),
    mainPanel(
      leafletOutput("map", height = 500),
      br(),
      DT::dataTableOutput("results")
    )
  )
)

server <- function(input, output, session) {

  # Run the PyPSA model when the button is pressed.
  results <- eventReactive(input$run_model, {
    res <- run_pypsa_model(
      demand_Copenhagen = input$demand_Copenhagen,
      demand_Aarhus = input$demand_Aarhus,
      demand_Aalborg = input$demand_Aalborg,
      capacity_wind = input$capacity_wind,
      cost_wind = input$cost_wind,
      capacity_solar = input$capacity_solar,
      cost_solar = input$cost_solar,
      capacity_gas = input$capacity_gas,
      cost_gas = input$cost_gas
    )
    res
  })

  # Render a DataTable of generator outputs with improved column names.
  output$results <- DT::renderDataTable({
    req(results())
    gens <- results()$generators
    gen_names <- names(gens)

    # Split generator names into technology and location.
    tech <- sapply(gen_names, function(x) strsplit(x, "_")[[1]][1])
    loc <- sapply(gen_names, function(x) strsplit(x, "_")[[1]][2])

    # Capitalize the technology names.
    tech <- sapply(tech, function(x) {
      paste0(toupper(substring(x, 1, 1)), tolower(substring(x, 2)))
    })

    data <- data.frame(
      Technology = tech,
      Location = loc,
      `Output (MW)` = round(as.numeric(gens), 2),
      stringsAsFactors = FALSE,
      check.names = FALSE
    )

    datatable(data, options = list(pageLength = 5, dom = 't'), rownames = FALSE)
  })

  # Render the base Leaflet map with custom icons for each generation type.
  output$map <- renderLeaflet({
    # Define custom icons using awesomeIcons:
    # Wind: fa-wind, Solar: fa-sun, Gas: fa-fire.
    gen_icons <- awesomeIcons(
      icon = c("fa-leaf", "fa-sun-o", "fa-fire"),
      markerColor = c("blue", "blue", "blue"),
      library = "fa"
    )

    leaflet() %>%
      addTiles() %>%
      setView(lng = 10, lat = 56, zoom = 6) %>%
      addAwesomeMarkers(
        lng = c(12.5683, 10.2039, 9.9217),
        lat = c(55.6761, 56.1629, 57.0488),
        popup = c("Copenhagen (Wind)", "Aarhus (Solar)", "Aalborg (Gas)"),
        icon = gen_icons
      )
  })

  # Update the map with transmission lines when new results are available.
  observeEvent(results(), {
    res <- results()
    buses <- res$buses
    # Transmission lines as defined in the Python model.
    lines_list <- list(
      list(from = "Copenhagen", to = "Aarhus"),
      list(from = "Aarhus", to = "Aalborg"),
      list(from = "Aalborg", to = "Copenhagen")
    )

    leafletProxy("map") %>%
      clearShapes()

    for (line in lines_list) {
      from_bus <- line$from
      to_bus <- line$to
      lat1 <- buses[[from_bus]]$lat
      lng1 <- buses[[from_bus]]$lon
      lat2 <- buses[[to_bus]]$lat
      lng2 <- buses[[to_bus]]$lon

      leafletProxy("map") %>%
        addPolylines(lng = c(lng1, lng2),
                     lat = c(lat1, lat2),
                     color = "blue",
                     weight = 3,
                     opacity = 0.7)
    }
  })
}

shinyApp(ui, server)
