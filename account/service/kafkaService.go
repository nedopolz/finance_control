package service

import (
	"context"
	"github.com/nedopolz/financecontrol/models"
	pb "github.com/nedopolz/financecontrol/proto-definitions"
	"github.com/segmentio/kafka-go"
	"google.golang.org/protobuf/proto"
	"log"
	"strconv"
)

type KafkaService struct {
	Kafka *kafka.Writer
}

func (k *KafkaService) SendMessage(user models.User) bool {
	msg := &pb.UserCreatedMessage{
		ExternalID: strconv.Itoa(int(user.ID)),
		Email:      user.Email,
		Username:   user.Username,
	}
	buff, err := proto.Marshal(msg)
	if err != nil {
		return false
	}
	err = k.Kafka.WriteMessages(context.Background(), kafka.Message{Value: buff})
	if err != nil {
		log.Fatal("failed to write messages:", err)
		return false
	}
	return true
}
