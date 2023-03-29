package main

import (
	"github.com/gin-gonic/gin"
	"github.com/nedopolz/financecontrol/controllers"
	"github.com/nedopolz/financecontrol/initializers"
	"github.com/sirupsen/logrus"
)

func init() {
	initializers.LoadEnvVariables()
	initializers.ConnectToDB()
	initializers.SyncDB()
}

func main() {
	logrus.SetFormatter(new(logrus.JSONFormatter))
	app := gin.Default()
	app.GET("/health", controllers.Health)
	app.POST("/signup", controllers.Signup)
	app.POST("/login", controllers.Login)
	app.Run("127.0.0.1:8003")
}
