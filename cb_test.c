```
#include <stdio.h>
 
typedef void (*callback_func)(int len, char* packet);
 
callback_func g_cb_func;
 
typedef struct _my_ops_t {
    callback_func cb1;
    callback_func cb2;
}my_ops_t;
 
my_ops_t* g_my_ops;
 
void func1(int len, char *packet)
{
    printf("call: %s(%d, %s)\n", __func__, len, packet);
}
 
void func2(int len, char *packet)
{
    printf("call: %s(%d, %s)\n", __func__, len, packet);
}
 
my_ops_t my_ops = {
    .cb1 = func1,
    .cb2 = func2,
};
 
void register_ops(my_ops_t* my_ops)
{
    g_my_ops = my_ops;
}
 
/*-------------------------------------------------------------*/
 
typedef struct _isp_msg_t {
    int msg_size;
    int api_name;
    int flag;
}isp_msg_t;
 
void my_init()
{
    printf("call:%s\n", __func__);
}
 
void my_flush(isp_msg_t *msg, int type)
{
    msg->flag = type;
    printf("call:%s(*msg, %d)\n", __func__, type);
    printf("msg->msg_size:%d\n", msg->msg_size);
    printf("msg->api_name:%d\n", msg->api_name);
    printf("msg->flag:%d\n", msg->flag);
}
 
typedef struct _df_ops_t {
    int status;
    void (*flush)(isp_msg_t *msg, int type);
    void (*init)(void);
}df_ops_t;
 
df_ops_t *g_df_ops;
 
df_ops_t my_df_ops = {
    .flush = my_flush,
    .init = my_init,
};
 
void register_df_ops(df_ops_t *ops)
{
    g_df_ops = ops;
}
 
int main(int argc, char const *argv[])
{
    register_ops(&my_ops);
    g_my_ops->cb1(1, "123");
    g_my_ops->cb2(2, "246");
 
 
    isp_msg_t msg = {
        .msg_size = 20,
        .api_name = 10,
    };
 
    register_df_ops(&my_df_ops);
    g_df_ops->init();
    g_df_ops->flush(&msg, 2);
 
    return 0;
}
```
