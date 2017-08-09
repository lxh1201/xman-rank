//author : muhe

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char name[32];
char *ptr[10];
char ptr_num = 0;

int menu(){
    write(1,"1.Add    order\n",strlen("1.Add    order\n"));
    write(1,"2.Show   order\n",strlen("2.Show   order\n"));
    write(1,"3.Edit   order\n",strlen("3.Edit   order\n"));
    write(1,"4.Delete order\n",strlen("4.Delete order\n"));
    write(1,"5.Exit\n",strlen("5.Exit\n"));
}

int get_name(){
    memset(name,0,32);
    write(1,"What's your name:",strlen("What's your name:"));
    return read(0,name,31);
}

int add_order(){
    int res;
    char *s;
    if(ptr_num <0 || ptr_num >10){
        res = write(1,"Order full!\n",strlen("Order full!\n"));
    }else{
        s = malloc(32);
        if(!s){
            write(1,"malloc error!\n",strlen("malloc error!\n"));
            exit(0);
        }
        memset(s,0,32);
        read(0,s,31);
        res = ptr_num++;
        ptr[res] = s;
    }
    return res;
}

int show_order(){
    int res,index;
    write(1,"Input the order index:",strlen("Input the order index:"));
    index = get_choice();
    if(index <0 || index >10){
        res = write(1,"Error\n",strlen("Error\n"));
    }else{
        //res = printf("%s",(ptr[index]));
        res = write(1,ptr[index],31);
    }
    return res;
}

int edit_order(){
    int res,index;
    write(1,"Input the order index:",strlen("Input the order index:"));
    index = get_choice();
    if(index <0 || index >10){
        res = write(1,"Error\n",strlen("Error\n"));
    }else{
        res = read(0,(ptr[index]),31);
    }
    return res;
}

void del_order(){
    int index;
    write(1,"Input the order index:",strlen("Input the order index:"));
    index = get_choice();
    if(index <0 || index >10){
        write(1,"Error\n",strlen("Error\n"));
    }else{
        free(ptr[index]);
    }
}

int get_choice(){
    char ch[2];
    read(0,ch,2);
    return atoi(ch);
}

int main(int argc, char const *argv[]) {
    setbuf(stdin,NULL);
    setbuf(stdout,NULL);

    write(1,"Welcome to MY-SHOP\n",strlen("Welcome to MY-SHOP\n"));
    get_name();

    while (1) {
        menu();
        switch (get_choice()) {
            case 1:
                add_order();
                break;
            case 2:
                show_order();
                break;
            case 3:
                edit_order();
                break;
            case 4:
                del_order();
                break;
            case 5:
                exit(0);
                return;
            default:
                write(1,"Opt error!\n",strlen("Opt error!\n"));
                break;
        }
    }
    return 0;
}
