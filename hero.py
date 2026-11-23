class Hero:
    # 【类变量】所有对象共享的数据。代表整个服务器的基础信息
    server_name = "一区-艾泽拉斯"
    total_heroes = 0  # 记录一共创建了多少个角色

    def __init__(self, name, hp):
        # 【对象特有属性】每个角色都有自己独立的名字和血量
        self.name = name
        self.__hp = hp  # 【封装】前面加__，变成私有属性，外部不能随便改，防止开挂直接改血
        Hero.total_heroes += 1  # 【类与对象互动】每创建一个对象，总数+1

    def __del__(self):
        # 【析构函数】当对象被销毁（比如角色被删除）时自动调用
        Hero.total_heroes -= 1

    def get_hp(self):
        # 【封装】提供一个正规渠道查看血量
        return self.__hp

    def take_damage(self, damage):
        # 【封装】提供正规渠道扣血，并且内部做逻辑判断，不能扣成负数
        self.__hp -= damage
        if self.__hp < 0:
            self.__hp = 0
        print(f"{self.name} 受到了 {damage} 点伤害，剩余血量：{self.__hp}")

    def attack(self):
        # 【多态】父类提供了一个基础攻击动作
        print(f"{self.name} 发起了一次普通攻击！")

    # 【类方法】专门用来操作类变量（所有对象共享的数据）
    @classmethod
    def show_server_info(cls):
        print(f"当前服务器：{cls.server_name}，共有 {cls.total_heroes} 名玩家在线。")


# ======= 下面是【继承】和【多态】 =======
class Warrior(Hero):  # 战士【继承】了英雄
    def attack(self):
        # 【多态】重写父类方法，战士攻击方式不同
        print(f"战士 {self.name} 挥舞大刀，使用了【旋风斩】！")


class Mage(Hero):  # 法师【继承】了英雄
    def attack(self):
        # 【多态】重写父类方法，法师攻击方式不同
        print(f"法师 {self.name} 吟唱咒语，使用了【火球术】！")


# ================= 测试运行 =================
if __name__ == "__main__":
    # 【对象实例化】根据类（图纸）造出具体的对象
    h1 = Hero("平民玩家", 100)
    w1 = Warrior("盖伦", 200)
    m1 = Mage("安琪拉", 80)

    # 【封装测试】不能直接改血量，必须通过方法
    w1.take_damage(50) 
    # print(w1.__hp)  # 如果你把这行注释解开，会报错，因为私有属性被保护了

    # 【多态测试】把不同的角色放进同一个列表，统一发号施令
    team = [h1, w1, m1]
    for hero in team:
        hero.attack()  # 同一句代码，不同角色打出不同操作

    # 【类方法测试】
    Hero.show_server_info()

    # 【对象销毁】把法师删掉，析构函数触发，总人数-1
    del m1
    Hero.show_server_info()