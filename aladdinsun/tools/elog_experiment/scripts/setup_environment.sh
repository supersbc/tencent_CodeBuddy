#!/bin/bash
# E-Log实验环境搭建脚本

set -e

echo "================================================================================"
echo "E-Log 实验环境搭建"
echo "================================================================================"

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 检查Docker是否安装
check_docker() {
    echo -e "\n${YELLOW}[1/6] 检查Docker...${NC}"
    if ! command -v docker &> /dev/null; then
        echo -e "${RED}错误: Docker未安装${NC}"
        echo "请先安装Docker: https://docs.docker.com/get-docker/"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker已安装: $(docker --version)${NC}"
}

# 检查Docker Compose是否安装
check_docker_compose() {
    echo -e "\n${YELLOW}[2/6] 检查Docker Compose...${NC}"
    if ! command -v docker-compose &> /dev/null; then
        echo -e "${RED}错误: Docker Compose未安装${NC}"
        echo "请先安装Docker Compose: https://docs.docker.com/compose/install/"
        exit 1
    fi
    echo -e "${GREEN}✓ Docker Compose已安装: $(docker-compose --version)${NC}"
}

# 创建必要的目录
create_directories() {
    echo -e "\n${YELLOW}[3/6] 创建目录结构...${NC}"
    
    mkdir -p data/{confignode,datanode1,datanode2,datanode3,prometheus,grafana}
    mkdir -p logs/{confignode,datanode1,datanode2,datanode3}
    mkdir -p data/{raw_logs,parsed_logs,results,metrics}
    
    echo -e "${GREEN}✓ 目录创建完成${NC}"
}

# 拉取Docker镜像
pull_images() {
    echo -e "\n${YELLOW}[4/6] 拉取Docker镜像...${NC}"
    
    echo "拉取Apache IoTDB镜像..."
    docker pull apache/iotdb:1.2.2
    
    echo "拉取Prometheus镜像..."
    docker pull prom/prometheus:latest
    
    echo "拉取Grafana镜像..."
    docker pull grafana/grafana:latest
    
    echo -e "${GREEN}✓ 镜像拉取完成${NC}"
}

# 启动IoTDB集群
start_cluster() {
    echo -e "\n${YELLOW}[5/6] 启动IoTDB集群...${NC}"
    
    # 停止已存在的容器
    docker-compose down 2>/dev/null || true
    
    # 启动集群
    docker-compose up -d
    
    echo "等待集群启动..."
    sleep 30
    
    echo -e "${GREEN}✓ IoTDB集群已启动${NC}"
}

# 验证集群状态
verify_cluster() {
    echo -e "\n${YELLOW}[6/6] 验证集群状态...${NC}"
    
    # 检查容器状态
    echo "容器状态:"
    docker-compose ps
    
    # 等待数据节点就绪
    echo -e "\n等待数据节点就绪..."
    max_retries=30
    retry=0
    
    while [ $retry -lt $max_retries ]; do
        if docker exec iotdb-datanode-1 bash -c "echo 'show cluster' | /iotdb/sbin/start-cli.sh -h localhost -p 6667" &>/dev/null; then
            echo -e "${GREEN}✓ 集群就绪${NC}"
            break
        fi
        retry=$((retry+1))
        echo "等待中... ($retry/$max_retries)"
        sleep 2
    done
    
    if [ $retry -eq $max_retries ]; then
        echo -e "${RED}错误: 集群启动超时${NC}"
        exit 1
    fi
    
    # 显示集群信息
    echo -e "\n集群信息:"
    docker exec iotdb-datanode-1 bash -c "echo 'show cluster' | /iotdb/sbin/start-cli.sh -h localhost -p 6667" || true
}

# 安装Python依赖
install_python_deps() {
    echo -e "\n${YELLOW}安装Python依赖...${NC}"
    
    if command -v pip3 &> /dev/null; then
        pip3 install -r requirements.txt
        echo -e "${GREEN}✓ Python依赖安装完成${NC}"
    else
        echo -e "${YELLOW}警告: pip3未找到，请手动安装Python依赖${NC}"
    fi
}

# 显示访问信息
show_info() {
    echo -e "\n================================================================================"
    echo -e "${GREEN}环境搭建完成！${NC}"
    echo "================================================================================"
    echo ""
    echo "IoTDB集群访问信息:"
    echo "  - 数据节点1: localhost:6667"
    echo "  - 数据节点2: localhost:6668"
    echo "  - 数据节点3: localhost:6669"
    echo "  - 用户名: root"
    echo "  - 密码: root"
    echo ""
    echo "监控访问信息:"
    echo "  - Prometheus: http://localhost:9090"
    echo "  - Grafana: http://localhost:3000 (admin/admin)"
    echo ""
    echo "连接示例:"
    echo "  docker exec -it iotdb-datanode-1 /iotdb/sbin/start-cli.sh -h localhost -p 6667"
    echo ""
    echo "下一步:"
    echo "  1. 运行TSBS基准测试: bash scripts/run_tsbs.sh"
    echo "  2. 运行实验: python3 scripts/run_experiment.py"
    echo "  3. 运行演示: python3 demo_experiment.py"
    echo ""
    echo "停止集群:"
    echo "  docker-compose down"
    echo ""
    echo "查看日志:"
    echo "  docker-compose logs -f"
    echo "================================================================================"
}

# 主函数
main() {
    cd "$(dirname "$0")/.."
    
    check_docker
    check_docker_compose
    create_directories
    pull_images
    start_cluster
    verify_cluster
    install_python_deps
    show_info
}

# 运行主函数
main
