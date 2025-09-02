#include<stdio.h>
int main(){
    int arr[]={1,2,3,4,5};
    int n=sizeof(arr)/sizeof(arr[0]);
    int insertindex=2;
    int newelement=9;
    int update[n+1];
    for(int i=0;i<n;i++){
        update[i]=arr[i];
    }
    update[insertindex]=newelement;
    for(int i=insertindex;i<n;i++){
        update[i+1]=arr[i];


    }
    for(int i=0;i<n+1;i++){
        printf("%d",update[i]);
    }
    return 0;


}