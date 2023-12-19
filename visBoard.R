library(ggplot2)
library(shiny)
library(shinydashboard)
library(DT)
data <- read.csv("./Video_Games_Sales_as_at_22_Dec_2016.csv")

ui <- dashboardPage(skin = "purple",
  dashboardHeader(title = "Games Sales",
    dropdownMenu(type = "messages",
      messageItem(
        from = "Update",
        message = "Dashboard have been changed",
        icon = icon("sign-out"),
        time = "00:00 01-01-2024"
      ),
      messageItem(
        from = "New Data",
        message = "How do I add entries?",
        icon = icon("question"),
        time = "23:23 24-12-2023"
      ),
      messageItem(
        from = "Support",
        message = "The new account is ready.",
        icon = icon("life-ring"),
        time = "05:00 14-12-2023"
      )
    ),
    dropdownMenu(type = "notifications",
      notificationItem(
        text = "5 active users",
        icon("users")
      ),
      notificationItem(
        text = "12 entries registred",
        icon("truck"),
        status = "success"
      ),
      notificationItem(
        text = "Server about to explode",
        icon = icon("exclamation-triangle"),
        status = "warning"
      )
    ),
    dropdownMenu(type = "tasks", badgeStatus = "success",
      taskItem(value = 2, color = "green",
        "Documentation"
      ),
      taskItem(value = 75, color = "aqua",
        "Code"
      ),
      taskItem(value = 40, color = "yellow",
        "Questions"
      ),
      taskItem(value = 35, color = "red",
        "Overall project"
      )
    )
  ),
  dashboardSidebar(
    sidebarMenu(
      menuItem("Overview", tabName = "overview", icon = icon("dashboard"),
               menuSubItem("Distribution", tabName = "distribution"),
               menuSubItem("Evolution", tabName = "evolution")),
      menuItem("Statistics", tabName = "statistics", icon = icon("th")),
      menuItem("DataTable", tabName = "dataTable", icon = icon("th")),
      menuItem("Upload", tabName = "upload", icon = icon("th")),
      menuItem("Source code", icon = icon("file-code-o"), href = "https://github.com/martinloevborg/Data-Visualization-project")
    )
  ),
  dashboardBody(
    tabItems(
      tabItem(tabName = "distribution",
        fluidRow(height = 200,
          box(title = "Controls",
            selectInput(inputId = "y", 
                        label = "Y-axis:",
                        choices = c("Critic_Score", "Critic_Count", "User_Score", "User_Count"), 
                        selected = "Critic_Score"),
            selectInput(inputId = "x", 
                        label = "X-axis:",
                        choices = c("Critic_Score", "Critic_Count", "User_Score", "User_Count"), 
                        selected = "Critic_Count"),
          ),
          box(plotOutput(outputId = "scatterplot", height = 200))
        ),
        fluidRow(
          box(title = "First plot", plotOutput("plot3", height = 200)),
          tabBox(
            title = tagList(shiny::icon("gear"), "Scatter plot"),
            id = "tabset1", height = "250px", 
            side = "right", selected = "Tab2",
            tabPanel("Tab1", plotOutput("plot", height = 200)),
            tabPanel("Tab2", plotOutput("plot2", height = 200))
          )
        )
      ),
      tabItem(tabName = "evolution",
        h2("Pie chart, Line and Barplot")
      ),
      tabItem(tabName = "statistics",
        fluidRow(
          infoBox("Mean", 10 * 2, icon = icon("credit-card")),
          infoBox("SD", 5 * 5,icon = icon("list"), color = "purple"),
          infoBox("Median", "80%", icon = icon("thumbs-up", lib = "glyphicon"), color = "yellow")
        ),
        fluidRow(
          infoBox("Mean", 10 * 2, icon = icon("credit-card"), fill = TRUE),
          infoBox("SD", 5 * 5, icon = icon("list"), color = "purple", fill = TRUE),
          infoBox("Median", "80%", icon = icon("thumbs-up", lib = "glyphicon"), color = "yellow", fill = TRUE)
        ),
        fluidRow(
          valueBox(10 * 2, "Mean", icon = icon("credit-card")),
          valueBox(5 * 5,"SD", icon = icon("list"), color = "purple"),
          valueBox("80%", "Median", icon = icon("thumbs-up", lib = "glyphicon"), color = "yellow")
        ),
        box(
          title = "Boxplot", status = "warning", solidHeader = TRUE,
          collapsible = TRUE, background = "black",
          plotOutput("plot4", height = 200)
        )
      ),
      tabItem(tabName = "dataTable",
        h2("Showcase of data set"),
        checkboxGroupInput("show_vars", "Parameters",
                           names(data), selected = names(data), inline = TRUE),
        DT::dataTableOutput("mytable")
      ),
      tabItem(tabName = "upload",
        h2("Option to upload data"),
        fileInput("fileId", h3("File input"), accept = ".csv"),
        tableOutput("contents")
      )
    )
  )
)

server <- function(input, output){
  output$plot <- renderPlot({
    ggplot(data = data, aes(x=User_Count, y=User_Score, size=Global_Sales, color=Genre)) + geom_point()
  })
  output$plot2 <- renderPlot({
    ggplot(data = data, aes(x=User_Count, y=User_Score)) + geom_point()
  })
  output$plot3 <- renderPlot({
    ggplot(data = data, aes(x=Critic_Score)) + geom_histogram()
  })
  output$plot4 <- renderPlot({
    ggplot(data = data, aes(x=Genre, y=Critic_Count)) + geom_boxplot()
  })
  
  #---
  
  output$scatterplot <- renderPlot({
    ggplot(data = data, aes_string(x = input$x, y = input$y)) + geom_point()
  })
  output$mytable = DT::renderDataTable({
    DT::datatable(data[, input$show_vars, drop = FALSE])
  })
  output$contents <- renderTable({
    fileVar <- input$fileId
    req(fileVar)
    read.csv(fileVar$datapath)
  })
}

shinyApp(ui, server)
