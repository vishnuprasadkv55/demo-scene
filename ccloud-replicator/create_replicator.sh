#!/bin/bash

source .env

epoch=$(date +%s)

curl -s -X PUT -H "Accept:application/json" \
    -H  "Content-Type:application/json" "http://localhost:58083/connectors/replicator-source"$epoch"/config" \
    -d '
        {
        "connector.class"             : "io.confluent.connect.replicator.ReplicatorSourceConnector",
        "key.converter"               : "io.confluent.connect.replicator.util.ByteArrayConverter",
        "value.converter"             : "io.confluent.connect.replicator.util.ByteArrayConverter",
        "header.converter"            : "io.confluent.connect.replicator.util.ByteArrayConverter",
        "src.kafka.bootstrap.servers" : "'$CCLOUD_BROKER_HOST'",
        "src.kafka.security.protocol" : "SASL_SSL",
        "src.kafka.sasl.mechanism"    : "PLAIN",
        "src.kafka.sasl.jaas.config"  : "org.apache.kafka.common.security.plain.PlainLoginModule required username=\"'$CCLOUD_API_KEY'\" password=\"'$CCLOUD_API_SECRET'\";",
        "src.consumer.group.id"       : "replicator-'$epoch'",
        "dest.kafka.bootstrap.servers": "kafka-1:39092,kafka-2:49092,kafka-3:59092",
        "topic.whitelist"             : "test_topic",
        "topic.rename.format"         :"${topic}",
        "confluent.license"           :"",
        "confluent.topic.bootstrap.servers":"kafka-1:39092,kafka-2:49092,kafka-3:59092",
        "confluent.topic.replication.factor":1,
        "offset.start"                :"consumer"
        }'
