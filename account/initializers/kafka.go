package initializers

import (
	"context"
	"github.com/nedopolz/financecontrol/service"
	"github.com/segmentio/kafka-go"
	"github.com/sirupsen/logrus"
	"net"
	"os"
	"strconv"
)

var KafkaService service.KafkaService

func ConnectToKafka() {
	host := os.Getenv("KAFKA_HOST")
	topic := os.Getenv("KAFKA_TOPIC")

	// TODO deleteIT

	conn, err := kafka.Dial("tcp", host)
	if err != nil {
		panic(err.Error())
	}

	defer conn.Close()

	controller, err := conn.Controller()
	if err != nil {
		panic(err.Error())
	}

	controllerConn, err := kafka.Dial("tcp", net.JoinHostPort(controller.Host, strconv.Itoa(controller.Port)))
	if err != nil {
		panic(err.Error())
	}

	defer controllerConn.Close()

	topicConfigs := []kafka.TopicConfig{{Topic: topic, NumPartitions: 1, ReplicationFactor: 1}}

	err = controllerConn.CreateTopics(topicConfigs...)
	if err != nil {
		panic(err.Error())
	}

	kafkaWriter := &kafka.Writer{
		Addr:  kafka.TCP(host),
		Topic: topic,
	}

	KafkaService = service.KafkaService{Kafka: kafkaWriter}

	err = kafkaWriter.WriteMessages(context.Background(), kafka.Message{
		Value: []byte("test message"),
	})

	if err != nil {
		logrus.Panic(err)
	}
}
