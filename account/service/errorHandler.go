package service

import (
	"github.com/gin-gonic/gin"
	"github.com/sirupsen/logrus"
)

type jsonerror struct {
	Message string `json:"message"`
}

type CustomError struct {
	StatusCode   int
	Error        error
	VisibleError string
}

var NoError = CustomError{}

func NewErrorResponse(c *gin.Context, err CustomError) {
	if err.Error != nil {
		logrus.Info(err.Error.Error())
	}
	c.AbortWithStatusJSON(err.StatusCode, jsonerror{err.VisibleError})
}
