import java.io.*;
import java.util.*;

public class Solution {

    public static void main(String[] args) throws Exception{
        /* Enter your code here. Read input from STDIN. Print output to STDOUT. Your class should be named Solution. */
        BufferedReader br = new BufferedReader(new InputStreamReader(System.in));
        String line = br.readLine();

        boolean result = esBalanceado(line);

        int parentesis = 0;
        int corchete = 0;
        int llave = 0;


        if(result){
            System.out.println("True");
        } else{
            System.out.println("False");
        }
    }

    public static boolean esBalanceado (String line){
        int n = line.length();
        if(n==1){
            return true;
        } else if(n==2){
            return (line.charAt(0)=='(' && line.charAt(1)==')') ||(line.charAt(0)=='[' && line.charAt(1)==']') ||(line.charAt(0)=='{' && line.charAt(1)=='}')
        } else{
                char toLookFor = '';
                char startingChar = line.charAt(0);
                if(startingChar==='('){
                    if(line.charAt(n-1)==')'){
                        return esBalanceado(line.substring(1,n-1));
                    }
                    else{
                        toLookFor = ')';
                    }
                } else if(startingChar=='{'){}
            else if(startingChar=='['){

            } else{
                return false;
            }
                Integer[] calculoBalance = calcularBalance(line);
                return calculoBalance[0]==0 && calculoBalance[1]==0 && calculoBalance[2]==0;
        }

    }

    public static Integer[] calcularBalance(String line){

    }
}