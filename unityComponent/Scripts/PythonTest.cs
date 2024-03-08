﻿using System.Collections;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;
using TMPro;
using UnityEngine.VFX;
using Display;
using System;
using UnityEditor.Search;
using FileLoaders;
using Playback;
using Settings;
using SMPLModel;
using Unity.VisualScripting;
namespace yoga{
public class PythonTest : MonoBehaviour
{
    //public String animationsFolder;
    
    //AnimationFileReference fileReference = new AnimationFileReference(animationsFolder, listFile);
    [SerializeField] AnimationListAsset animationListAsset;
    [SerializeField] PlaybackSettings playbackSettings = default;
    [SerializeField] Models modelTest;
    [SerializeField] BodySettings bodySettings;
    [SerializeField] DisplaySettings displaySettings;
    [SerializeField] VisualEffect meshVisual;
    //[SerializeField] VisualEffect JointVisual;
    List<List<AMASSAnimation>> animations;
    SUPPlayer player;
    GameObject nCharacter;
    Transform Pelvis;
    int currentlyPlayingIndex = 0;
    List<JointSphere> jointsList = new List<JointSphere>();
    List<JointSphere> orderJointsList = new List<JointSphere>();
    public List<VisualEffect> JointVisuals=new List<VisualEffect>();
    List<float> numbers = new List<float>();
    //public static event Action <float,int> GetFailedScore;
    string tempStr = "Sent from Python xxxx";
    int numToSendToPython = 0;
    UdpSocket udpSocket;
    string[] targetNames = {
     "JointSphere for R_Elbow", 
     "JointSphere for L_Elbow", 
     "JointSphere for R_Shoulder",
     "JointSphere for L_Shoulder",
     "JointSphere for R_Hip",
     "JointSphere for L_Hip",
     "JointSphere for R_Knee",
     "JointSphere for L_Knee"
      };
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
    void OnEnable()
    {
       // AnimationFileReference fileReference = new AnimationFileReference(animationsFolder);
        SUPLoader.LoadFromListAssetAsync(animationListAsset, DoneLoading);
        //SUPLoader.LoadAsync(fileReference, modelTest, playbackSettings, DoneLoading);
        player = new SUPPlayer(playbackSettings, displaySettings, bodySettings);
        // load animations from list asset
        ModelDefinition.OnCharacterInstantiated += HandleCharacterInstantiated;
       PointLightDisplay.ParticleAction+=ParticleCorrect;
       //there's not any jointSphere
    }
    void Start()
    {
        udpSocket = FindObjectOfType<UdpSocket>();
    }
    void Update()
    { 
    //SearchValue();
    attachParticles();
    meshAttach();   
      if (Input.GetKeyDown(KeyCode.Space)) {
            // Stop currently playing animation
            player.StopCurrentAnimations();
            //Debug.Log("destroy the first character "+jointsList.Count);
            jointsList.Clear();
            orderJointsList.Clear();
            //Debug.Log("clean the list after destroying "+jointsList.Count);
            // Increment our animation index
            currentlyPlayingIndex++;
            // If reached end, restart all.
            if (currentlyPlayingIndex >= animations.Count) currentlyPlayingIndex = 0;
            // Play the next animation
            player.Play(animations[currentlyPlayingIndex]);
            PointLightDisplay.ParticleAction+=ParticleCorrect;
            Debug.Log("第二次原本载入的球总共数量是："+jointsList.Count);
            foreach(JointSphere j in jointsList)
            {
            Debug.Log("第二次原本载入的球名字是："+j.name);
            }
            sortOrder();
             foreach(JointSphere j in orderJointsList)
            {
            Debug.Log("第二次重新排序的球的名字是："+j.name);
            }
           
        
        } 
    }
    void DoneLoading(List<List<AMASSAnimation>> loadedAnimations) {
        
        this.animations = loadedAnimations;
       // Debug.Log("animation Size:"+animations.Count);
        // Start playing first animation when loading complete
        player.Play(animations[0]);
        sortOrder();
        // Debug.Log("First orderedjointsList 数量："+orderJointsList.Count);
        // foreach(JointSphere j in orderJointsList)
        // {
        // Debug.Log("初始化重新排序的球的名字是："+j.name);
        // }
    }
    
    void SearchValue()
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
                                    // Debug.Log("passing value: "+numbers[i]);
                                    // Debug.Log("passing index: "+i);
                                    JointVisuals[i].SetFloat("particleSize",numbers[i]*0.1f);
                                    JointVisuals[i].SetVector3("colorControl",new Vector3(1.0f,0.0f,0.0f));
                                   //attachTag(i);
                                }
                        }
                numbers.Clear();
                }
            }
        }
    }
    // void attachTag(int i)
    // {
    // switch(i)
    //     case 0:
            
    //         break;
    // }
  
    /// TODO:但是生成球的顺序不匹配

    void meshAttach()
    {
    if(nCharacter != null)
    {
    meshVisual.SetVector3("MeshTransform_position", Pelvis.position);
     meshVisual.SetVector3("MeshTransform_angles", Pelvis.eulerAngles);
     meshVisual.SetVector3("MeshTransform_scale", Pelvis.localScale);
    }
    }
    void attachParticles()
    {
        if(jointsList.Count==8)
        {
            for(int i=0;i<JointVisuals.Count;++i)
            {
            //JointVisuals[i].SetFloat("particleSize",numbers[i]*0.1f);
            //Debug.Log("jointsList: "+jointsList[i].gameObject.transform.position);
            JointVisuals[i].SetVector3("jointTransform_position", jointsList[i].gameObject.transform.position);
            JointVisuals[i].SetVector3("jointTransform_angles", jointsList[i].gameObject.transform.eulerAngles);
            JointVisuals[i].SetVector3("jointTransform_scale", jointsList[i].gameObject.transform.localScale);

            }
        }
        
    }
    void HandleCharacterInstantiated(GameObject newCharacter)
    {
        nCharacter = newCharacter;
        //Debug.Log("nCharacter.name"+nCharacter.transform.GetChild(0).GetChild(0).gameObject.GetComponent<SkinnedMeshRenderer>());
        SkinnedMeshRenderer skin1 = nCharacter.transform.GetChild(0).GetChild(0).gameObject.GetComponent<SkinnedMeshRenderer>();
        meshVisual.SetSkinnedMeshRenderer("SkinnedMeshRenderer", skin1);
        GameObject mesh = newCharacter.transform.GetChild(0).GetChild(0).gameObject;
        Pelvis = newCharacter.transform.GetChild(0).GetChild(1);
    }
    void ParticleCorrect(JointSphere jSphere)
    {
     if(jSphere.isMark==true)
        {
            jointsList.Add(jSphere);
            
        }

    }
    void sortOrder()
    {
    Debug.Log("排序启动");
    if(jointsList.Count==8)
    {
     foreach (string targetName in targetNames)
        {
            for (int i = 0; i < jointsList.Count; i++)
            {
                if (jointsList[i].name == targetName)
                {
                    orderJointsList.Add(jointsList[i]); // 将满足条件的元素加入新列表
                    
                }
            }
        }
    }
    
    }        
}
}

