package service

import (
	"fmt"
	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"github.com/nedopolz/financecontrol/controllers/schemas"
	"github.com/nedopolz/financecontrol/models"
	"golang.org/x/crypto/bcrypt"
	"gorm.io/gorm"
	"os"
	"strconv"
)

type UserManager struct {
	DB *gorm.DB
}

func (m *UserManager) CreateUser(userdata schemas.UserSignUp) CustomError {
	hash, err := bcrypt.GenerateFromPassword([]byte(userdata.Password), 10)
	if err != nil {
		return CustomError{
			StatusCode:   400,
			VisibleError: "unable to hash password",
			Error:        fmt.Errorf("error=%s on password=%s hashing", err.Error(), userdata.Password),
		}
	}
	user := models.User{Email: userdata.Email, Username: userdata.Username, Password: string(hash)}
	result := m.DB.Create(&user)
	if result.Error != nil {
		return CustomError{
			StatusCode:   400,
			Error:        result.Error,
			VisibleError: "not unique",
		}
	}
	return CustomError{}
}

func (m *UserManager) LoginUser(c *gin.Context, userdata schemas.UserLogin) (string, CustomError) {
	var user models.User
	m.DB.First(&user, "username = ?", userdata.Username)
	if user.ID == 0 {
		return "", CustomError{StatusCode: 404, VisibleError: "invalid username or password", Error: nil}
	}
	err := bcrypt.CompareHashAndPassword([]byte(user.Password), []byte(userdata.Password))
	if err != nil {
		return "", CustomError{StatusCode: 404, VisibleError: "invalid username or password", Error: nil}
	}
	token := jwt.NewWithClaims(jwt.SigningMethodHS256, jwt.MapClaims{
		"sub": strconv.FormatInt(int64(user.ID), 10),
	})
	token.Header["kid"] = "sim2"
	secret := os.Getenv("JWT_SECRET")
	tokenString, err := token.SignedString([]byte(secret))

	if err != nil {
		err = fmt.Errorf("for userID=%d error in json token generation", user.ID)
		return "", CustomError{StatusCode: 400, VisibleError: "failed to create token", Error: err}
	}

	return tokenString, CustomError{}
}
