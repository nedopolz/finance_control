//DO NOT USE IN PRODUCTION

package initializers

import (
	"github.com/nedopolz/financecontrol/models"
	"github.com/sirupsen/logrus"
)

func SyncDB() {
	err := DB.AutoMigrate(&models.User{})
	if err != nil {
		logrus.Panic("Unsuccessful DB tables initialisation")
	}
}
