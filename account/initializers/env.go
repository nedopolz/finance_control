package initializers

import (
	"github.com/sirupsen/logrus"

	"github.com/joho/godotenv"
)

func LoadEnvVariables() {
	err := godotenv.Load()

	if err != nil {
		logrus.Panic("Error loading .env file")
	}
}
