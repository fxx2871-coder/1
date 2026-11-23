#include <iostream>
#include <string>
using namespace std;

class Hero {
private:
    // 【封装】私有属性，外部无法直接访问，只能通过 public 的接口
    int hp; 

public:
    string name; // 名字公开，方便直接读取

    // 【类变量】静态成员变量，所有对象共享
    static string serverName; 
    static int totalHeroes;

    // 构造函数：对象诞生时自动调用
    Hero(string n, int h) {
        name = n;
        hp = h;
        totalHeroes++; // 每 new 一个对象，总人数+1
    }

    // 析构函数：对象被 delete 销毁时自动调用
    ~Hero() {
        totalHeroes--;
    }

    // 【封装】提供一个安全读取血量的方法
    int getHp() {
        return hp;
    }

    // 【封装】提供安全修改血量的方法，内部有限制逻辑
    void takeDamage(int damage) {
        hp -= damage;
        if (hp < 0) hp = 0;
        cout << name << " 受到了 " << damage << " 点伤害，剩余血量：" << hp << endl;
    }

    // 【多态】必须加 virtual，允许子类重写
    virtual void attack() {
        cout << name << " 发起了一次普通攻击！" << endl;
    }

    // 【静态方法】专门用来操作静态成员变量
    static void showServerInfo() {
        cout << "当前服务器：" << serverName << "，共有 " << totalHeroes << " 名玩家在线。" << endl;
    }
};

// 静态成员变量必须在类外初始化
string Hero::serverName = "一区-艾泽拉斯";
int Hero::totalHeroes = 0;


// ======= 下面是【继承】和【多态】 =======
class Warrior : public Hero {  // 战士【继承】父类
public:
    // 构造函数：调用父类的构造函数
    Warrior(string n, int h) : Hero(n, h) {} 

    // 【多态】重写父类的 attack 方法
    void attack() override {
        cout << "战士 " << name << " 挥舞大刀，使用了【旋风斩】！" << endl;
    }
};

class Mage : public Hero {  // 法师【继承】父类
public:
    Mage(string n, int h) : Hero(n, h) {}

    // 【多态】重写父类的 attack 方法
    void attack() override {
        cout << "法师 " << name << " 吟唱咒语，使用了【火球术】！" << endl;
    }
};


int main() {
    // 【对象实例化】
    // 注意：为了体现多态，这里用父类指针指向子类对象
    Hero* h1 = new Hero("平民玩家", 100);
    Hero* w1 = new Warrior("盖伦", 200);
    Hero* m1 = new Mage("安琪拉", 80);

    // 【封装测试】
    w1->takeDamage(50); // 只能通过方法扣血
    // cout << w1->hp; // 解除注释会报错，因为 hp 是 private 的

    // 【多态测试】把不同的角色放进同一个数组，统一发号施令
    Hero* team[3] = { h1, w1, m1 };
    for (int i = 0; i < 3; i++) {
        team[i]->attack(); // 同一句代码，不同角色打出不同操作
    }

    // 【类方法测试】
    Hero::showServerInfo();

    // 【对象销毁】delete 掉法师，触发析构函数，总人数-1
    delete m1;
    Hero::showServerInfo();

    delete h1;
    delete w1;
    return 0;
}