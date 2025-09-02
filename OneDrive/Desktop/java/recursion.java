public class recursion{
    public static void main(String[] args) {
       int n;
        //increaseing(n);
      //  System.out.println(fact(5));
        calsum(5);
        System.out.println(calsum(5));
       
            }
            public static void increaseing(int n){
                if(n==1){
                    System.out.println(n);
                    return;
                }
                
                
                increaseing(n-1);
                System.out.println(n+ " ");
            }
            public static int fact(int n){
                if(n==0){
                    return 1;

                }
               int factnn_=fact(n-1);
               int factn=n*factnn_;
               return factn;


            }
            public static int calsum(int n){
                if(n==1){
                    return 1;

                }
                int sum1=calsum(n-1);
                int sum=n+sum1;
                return sum;

            }

}