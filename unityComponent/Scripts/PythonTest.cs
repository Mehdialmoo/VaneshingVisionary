using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;
using TMPro;
using UnityEngine.VFX;
using Display;
using System;
namespace yoga{
public class PythonTest : MonoBehaviour
{
    //[SerializeField] TextMeshProUGUI pythonRcvdText = null;
    //[SerializeField] TextMeshProUGUI sendToPythonText = null;
    List<float> numbers = new List<float>();
    //List<string> keys = new List<string>{"R_Hip","L_Hip","R_Shoulder","L_Shoulder","R_Knee","L_Knee","L_Elbow","R_Elbow"};
    public static event Action <float,int> GetFailedScore;
    string tempStr = "Sent from Python xxxx";
    int numToSendToPython = 0;
    UdpSocket udpSocket;

    public void QuitApp()
    {
        print("Quitting");
        Application.Quit();
    }

    public void UpdatePythonRcvdText(string str)
    {
        tempStr = str;   
       
    }
    public void SendToPython()
    {
        udpSocket.SendData("Sent From Unity: " + numToSendToPython.ToString());
        numToSendToPython++;
      
    }
    void Start()
    {
        udpSocket = FindObjectOfType<UdpSocket>();
        
    }
    void Update()
    { 
        Regex regex = new Regex(@"[-+]?\b\d+(\.\d+)?([eE][-+]?\d+)?\b");
        MatchCollection matches = regex.Matches(tempStr);
        
         foreach (Match match in matches)
        {
            float number;
            if (float.TryParse(match.Value, out number))
            {
                numbers.Add(number);
                //print the 8 numbers.
                if (numbers.Count == 8)
                {
                    for (int i = 0; i < numbers.Count; i++)
                        {
                            if(numbers[i]<=0.7)
                                {
                                    GetFailedScore?.Invoke(numbers[i],i);
                                    Debug.Log("传走的数值是多少: "+numbers[i]);
                                    Debug.Log("传走的index是多少: "+i);
                                }
                        }
                numbers.Clear();
                }
            }
        }
    }
           
}
}

