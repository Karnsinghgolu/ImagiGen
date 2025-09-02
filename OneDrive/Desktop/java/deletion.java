public class deletion {
    public static void main(String[] args) {
        int arr[]={1,2,3,4,5};
        int deletionindex=3;
        int[] update=new int[arr.length-1];
        for(int i=3;i<arr.length-1;i++){
            if(i<deletionindex){
                update[i]=arr[i];
            }else{
                 update[i]=arr[i+1];
                
            }
            


            }

        
        for(int i=0;i<arr.length;i++){
            System.out.println(update[i]);
        }

    }
    
}
