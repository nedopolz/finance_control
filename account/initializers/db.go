package initializers

import (
	"fmt"
	"github.com/nedopolz/financecontrol/service"
	"github.com/sirupsen/logrus"
	"gorm.io/driver/postgres"
	"gorm.io/gorm"
	"os"
)

var DB *gorm.DB

var UserService service.UserManager

func ConnectToDB() {
	var err error
	var dsn string

	dsn = fmt.Sprintf("host=%s user=%s password=%s dbname=%s port=%s",
		os.Getenv("DBHOST"),
		os.Getenv("DBUSER"),
		os.Getenv("DBPASS"),
		os.Getenv("DBNAME"),
		os.Getenv("DBPORT"))

	DB, err = gorm.Open(postgres.Open(dsn), &gorm.Config{})

	UserService = service.UserManager{DB: DB}

	if err != nil {
		logrus.Panic("Failed to connect to db")
	}
}
