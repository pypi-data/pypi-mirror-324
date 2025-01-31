# flask sqlalchemy 需要实现数据库模型 
主页价格图表上还要加上 情绪热度日历页 关联着几种币种 积极/消极(程度) x轴日期

我的三段投资可能有四段 然后每段投资成功交易 需要根据三个月或者6个月用户自定义,或者当前市场价格重新计算三段投支
当前市场行情是牛市 熊市 还是横盘调整阶段
不要觉得不可能 除非你埋伏点足够低
14.28=12月底 *sol  march-->eth
xrp ada 
doge
fet/arb
algo
tia
op
0.378

当你赚钱了 赶紧退场 准备好子弹 关键低价 立马出手 赌在最低时刻  存起来(不动极低价格买入)
4w 操作现金

2000机器操作
大饼8-10%(btc) 
优质二饼
(10-16%)
eth 

三饼
xrp(12%-25)
sol


对于庄家 类似交易所 机构 华尔街 交易员 和 散户 的博弈 防止 散户存在 做空 做多 推波助澜 等情况 这种如何量化 在牛市中 如何以一个上帝视角观察整个盘局  也是一种心理博弈 在平局普遍上涨的情况 来一个插针10min 下跌13%的情况防止散户做多 然后在全民普遍觉得大涨的情况 突然爆跌25% 然后横盘 接下来的情况会如何 然后在临近圣诞节前夕 今天是12月12日 距离1月15-20日 新支持加密货币总统川普上台即将开启大牛的情况下 在你的分析中是什么 参考大众心理学 和 资本博弈论 的上帝视角情况下
以下是按照您的表格格式对 Peanut the Squirrel (PNUT) 代币的分析：
详细说明
1. 主要特点：
Peanut the Squirrel（PNUT）是基于 Solana 区块链的 Meme 代币，旨在通过社区驱动的方式传播幽默和娱乐价值。
2. 发行量：
总供应量为 9.998589 亿枚，当前流通量与总供应量相同，表明所有代币已全部释放。
3. 历史价格表现：
历史最高价为 $2.44（记录于2024年11月14日），当前价格为 $1.28，约为历史最高价的52.5%，显示出中等增长潜力。
4. 锁仓与释放划：
由于所有代币已全部释放，当前不存在锁仓计划，评分中等（8分）。
5. 市值与稀缺性：
当前市值为 $11.07 亿，稀缺性评分中等（8分）。
6. 链上规模：
作为基于 Solana 的 Meme 代币，生态规模有限，评分中等（7分）。
7. 名人推荐和机构持仓：
暂无知名人士支持或公开推荐，机构持仓信息未披露，评分较低（名人推荐：5分；机构持仓：4分）。
8. FDV比率：
完全稀释估值（FDV）与当前市值相同，FDV比率为1，评分中等（4分）。
9. 供应与通胀
由于所有代币已全部释放，供应稳定，通胀风险较低，评分中等（3分）。
10. 是否有主链：
PNUT 基于 Solana 区块链，没有独立主链。
11. 综合评分：
综合考虑各项因素，总评分为 68 分。
0.68 上下起伏震荡 32 系数

根据业务需要我需要 定义买卖的时间段 用户可以自定义 3段或者4段或者6段 每段从24小时里面分割
然后针对不同的时序设置策略
比如一天的24小时分为6段就是 14-18,18-24,0-3,3-9,9-12,12-14
然后还需要一个策略表 定义不同的跌卖涨卖算法 比如4h的最高点跌10%买入 或者6h的2次波动下跌5% 连续2次 则买入,因为这个策略的不确定性质 如何存储到数据库中？其中存在计算,我是取价格和时间段表自定义函数么？

那个时间段只能是string类型么？这样拿出处理是不是不方便 然后给我返回完整的数据模型表

根据币种设置风险系数 
(跌8%买入 UP4%卖 跌8%买 涨4卖 跌8买 涨12卖  爹(2-3)买 涨(3-5)卖 持续4h 重新计算) 
1h 10% 跑 
4h 20%-30% 跑 12-16h 20% 跌7-8%  上涨4% 跌
不可能连续16h 涨  一般12h 最高

我还要定义一个模拟盘记录表 比如当前在用户表添加模拟盘用户钱包设置 和实盘钱包余额记录 在加一个开关字段 比如我现在设置10000usdt 然后进入策略开始进行数据模拟透支买卖,然后每次的自动交易记录 包括 后面的总收益 收益百分比 7天 半个月 1个月 3个月 半年收入百分比 总收益 等模拟记录 还有有个实盘记录表 如果用户开启开关 则连接币安api进行实盘操作 然后记录相关数据记录 
+++++++++++++++++++++++++++++++++++
二倍
btc 23000
eth 15000
sol 8000
十倍卖
ada 500
sui  200
sei  200
avax 2000
arb  200
near 400
五倍币
fet 1000
dot 1000
aave 1000
op 500
+++++++++++++++++++++++++++++++++++

+++++++++++++++++++++++++++++++++++
Web Search Assistant with Ollama

++++++++++++++++++++++++++++++++++++
chrome driver
https://googlechromelabs.github.io/chrome-for-testing/
https://googlechromelabs.github.io/chrome-for-testing/
++++++++++++++++++++++++++++++++++++

# 币表 
	记录着各种币 
	外键 币种 
	介绍
	发行时间
	外键 生态链
	外键 创始人

# Notable Figures Attention
# 币种表  coin 种类(分类) 
    大饼上涨山寨是根据板块轮动上涨不能死守一个币
	记录着 新型币 主流币,还是山寨币, 生态币 

# 投资价值评分
    知名人士关注度	
    投资机构关注度	
    创始团队知名度评分（1-100）	
    新闻关注热度评分（1-100）

# 用户表 网站的user表 
	用户名 
	密码
	关注币
	我的投资总额
	目标达到多少
	目标时间

# 透支周期表:
	投掷段数Stage 比如三段 每段价格3% 5% 8%的
	段1:百分比
	段2:百分比
	段3 etc 设置
	周期3个月/6个月/12/24个月

	
# Stage表
	外键用户id
	设置时间:
	当前市场价格

# 投资比例表：
	外键:我的投资总额
	记录着按 那种类型 所持比例 比如： 主流币 30% 山寨20% 新兴50%
	类型所持数量 比如主流选3个 山寨选2个币种 生态选2个 新兴选3个


# 创始人:
	创始人
	团队名称
	知名度
	

# 透支机构表:
	机构名称
	外键:机构所持币种
	持有量
	持有比例
	
# 生态链 
	记录那些生态链  

# 投资价值评估:(程序定期更新)
   币种id  知名人士关注度	 创始团队知名度评分（1-100）新闻关注热度评分（1-100）	投资价值评估 投资价值评估分数是一个表


## 服务器设置
```
redis_install(){
    echo "正在安装redis" && sleep 3s
    local redis_version=$1
        echo $redis_version
        local Redis=redis-$redis_version.tar.gz
        echo "$python"
        if [ -f "$pkg_dir$Redis" ];then
                echo " 文件 $Redis 找到 "
        else
                echo "文件 $Redis 不存在将自动下载" 
                if ! wget -c -t3 -T60 ${redis_root_url}/$Redis -P $pkg_dir/; then
            echo "Failed to download $Redis \n 下载$Redis失败, 请手动下载到${pkg_dir} \n please download it to ${pkg_dir} directory manually and try again."
            echo -e "请把下列安装包放到$pkg_dir目录下 \n\n " $$ sleep 2s
                        exit 1
        fi
        fi
    cd $pkg_dir && echo "正在执行Redis安装"
        tar -zxvf $Redis
        cd redis-$redis_version\
        make MALLOC=libc
        cd \src
        make install
        mkdir -p /etc/redis/
        cp $pkg_dir/redis-$redis_version/redis.conf /etc/redis/6379.conf
        cp $pkg_dir/redis-$redis_version/utils/redis_init_script /etc/init.d/redisd
        sed -i '2i\
        # chkconfig:   2345 90 10
        # description:  Redis is a persistent key-value database' /etc/init.d/redisd
        echo '''
        [Unit]
        Description=redis-server
        After=network.target

        [Service]
        #Type=forking
        ExecStart=/usr/local/bin/redis-server /etc/redis/6379.conf
        PrivateTmp=true

        [Install]
        WantedBy=multi-user.target
        ''' >> /lib/systemd/system/redis.service
        systemctl daemon-reload
        systemctl enable redis.service
        systemctl restart redis.service
}
```

## 防火墙权限
```
firewall-cmd --permanent --zone=public --add-port=38245/tcp
firewall-cmd --permanent --zone=public --add-port=57804/tcp
firewall-cmd --permanent --zone=public --add-port=9736/tcp
firewall-cmd --permanent --zone=public --add-forward-port=port=33789:proto=tcp:toport=3306
firewall-cmd --permanent --zone=public --add-forward-port=port=68789:proto=tcp:toport=9736 
```
