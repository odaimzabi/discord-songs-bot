#!/bin/bash
echo ECS_CLUSTER=${aws_ecs_cluster.discord_bot_cluster.name} >> /etc/ecs/ecs.config
