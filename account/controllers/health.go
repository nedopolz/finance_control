package controllers

import (
	"github.com/gin-gonic/gin"
	"net/http"
)

// TODO add more data to response e.g (DB connection, CPU&memory limits)

func Health(c *gin.Context) {
	c.JSON(http.StatusOK, gin.H{
		"status": "Ok",
	})
}
