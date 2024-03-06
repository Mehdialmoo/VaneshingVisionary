using UnityEngine;
using System;
using System.IO;
using System.Text.RegularExpressions;
using System.Collections;
// [System.Serializable]
// public class Scores
// {
//     public float[] score;
// }
public class JSONReader : MonoBehaviour
{    
 void Start()
    {
        string inputString = "{[score:0.1,0.4,0.5,0.6]}";

        // 定义一个正则表达式来匹配数字
        Regex regex = new Regex(@"[-+]?\b\d+(\.\d+)?([eE][-+]?\d+)?\b");

        // 使用正则表达式在输入字符串中查找匹配项
        MatchCollection matches = regex.Matches(inputString);

        // 遍历所有匹配项并打印它们
        foreach (Match match in matches)
        {
            Debug.Log("Matched number: " + match.Value);
        }
    }

//     public TextAsset jsonFile;
    
//     Scores scores;

//     void Update()
//     {
//         LoadJSON();
//     }

//     void LoadJSON()
//     {
//         scores = JsonUtility.FromJson<Scores>(jsonFile.text);
//         Debug.Log("jsonFile.text: "+jsonFile.text.GetType());
//         Debug.Log("scores: "+scores.GetType());

//             foreach (float score in scores.score)
//             {
//                 Debug.Log("Score: " + score);
//             }
//     }
   
 }