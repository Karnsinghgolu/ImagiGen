public class loops {
    public static void main(String[] args) {
            int arr[]={1,2,3,4,5};
            int insertindex=2;
            int newelement=6;
            int[] update=new int[arr.length+1];
            for(int i=0;i<arr.length;i++){
                update[i]=arr[i];

            }
            update[insertindex]=newelement;
            for(int i=insertindex;i<arr.length;i++){
                update[i+1]=arr[i];


            }
            for(int i=0;i<update.length;i++){
                System.out.println(update[i]);
            }



    }
    
}
