package controllers

import (
	"github.com/gin-gonic/gin"
	"github.com/nedopolz/financecontrol/controllers/schemas"
	"github.com/nedopolz/financecontrol/initializers"
	"github.com/nedopolz/financecontrol/service"
	"net/http"
)

func Signup(c *gin.Context) {
	var user schemas.UserSignUp
	if err := c.Bind(&user); err != nil {
		service.NewErrorResponse(c, service.CustomError{StatusCode: 404, VisibleError: err.Error()})
		return
	}
	if err := initializers.UserService.CreateUser(user); err.Error != nil {
		service.NewErrorResponse(c, err)
		return
	}
	c.JSON(http.StatusOK, gin.H{})
}

func Login(c *gin.Context) {
	var user schemas.UserLogin
	if err := c.Bind(&user); err != nil {
		service.NewErrorResponse(c, service.CustomError{StatusCode: 404, VisibleError: err.Error()})
		return
	}
	token, err := initializers.UserService.LoginUser(c, user)
	if err != (service.NoError) {
		service.NewErrorResponse(c, err)
		return
	}
	c.JSON(http.StatusOK, gin.H{
		"token": token,
	})

}
