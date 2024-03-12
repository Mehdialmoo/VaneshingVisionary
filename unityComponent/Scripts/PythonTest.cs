﻿using System.Collections.Generic;
using System.Text.RegularExpressions;
using UnityEngine;
using UnityEngine.VFX;
using Display;
using FileLoaders;
using Playback;
using Settings;
using SMPLModel;
using System.ComponentModel.Composition;
namespace yoga{
public class PythonTest : MonoBehaviour
{
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
    string preTrue="false";
    //public static event Action <float,int> GetFailedScore;
    string tempStr = "Sent from Python xxxx";
    //int numToSendToPython = 0;
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
      public Vector3 characterV3;

    public void UpdatePythonRcvdText(string str)
    {
        tempStr = str;   
       
    }
    public void SendToPython()
    {
        udpSocket.SendData("true");
        
      
    }
    void OnEnable()
    {
       // AnimationFileReference fileReference = new AnimationFileReference(animationsFolder);
        SUPLoader.LoadFromListAssetAsync(animationListAsset, DoneLoading);
        //SUPLoader.LoadAsync(fileReference, modelTest, playbackSettings, DoneLoading);
        player = new SUPPlayer(playbackSettings, displaySettings, bodySettings);
        // load animations from list asset
        ModelDefinition.OnCharacterInstantiated += HandleCharacterInstantiated;
        ModelDefinition.OnCharacterInstantiated+= ChangeTheCharacterPosition;
        PointLightDisplay.ParticleAction+=ParticleCorrect;

    }
    void Start()
    {
        udpSocket = FindObjectOfType<UdpSocket>();
    }
    void Update()
    { 
        attachParticles();
        //SearchValue();
        meshAttach();  
        nextAction();
    }
    void nextAction()
    {
    player.StopCurrentAnimations();
        jointsList.Clear();
        orderJointsList.Clear();
        currentlyPlayingIndex++;
        if (currentlyPlayingIndex >= animations.Count) currentlyPlayingIndex = 0;
        player.Play(animations[currentlyPlayingIndex]);
        sortOrder();
        attachParticles();
    
        
     

    }
    void DoneLoading(List<List<AMASSAnimation>> loadedAnimations) {
        
        this.animations = loadedAnimations;
        player.Play(animations[0]);
        sortOrder();
        //Debug.Log("DoneLoading之后传球列表有"+jointsList.Count+"个");
    }
    
    void SearchValue()
    {
    
    Regex regex = new Regex(@"([-+]?\d+(\.\d+)?([eE][-+]?\d+)?\b)|\b(true|false)\b");
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
                //attachParticles();
                    for (int i = 0; i < numbers.Count; i++)
                        {
                        //yellow->green //The closer to green means the smaller the accuracy value coming through.
                        JointVisuals[i].SetVector3("colorControl",new Vector3(1.0f*numbers[i],1.0f,0.0f));      
                        }
                numbers.Clear();
                }
            }
            else
            {
            if(match.Groups[4].Value=="true")
            {
                //Debug.Log("boolean value is :"+match.Groups[4].Value);
                SendToPython();
                if(preTrue=="false")
                {
                    Debug.Log("trigger");
                    nextAction();
                    
                    preTrue = match.Groups[4].Value;
                }   
            }
            else if(match.Groups[4].Value=="false")
            {
                
                preTrue="false";
                Debug.Log("boolean value is :"+match.Groups[4].Value);
                
            }
            }
        }
    }
    void ChangeTheCharacterPosition(GameObject newCharacter)
    {
        newCharacter.gameObject.transform.position=characterV3;
        Debug.Log("newCharacter: "+newCharacter.gameObject.transform.position);

    }
    
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
        if(orderJointsList.Count==8)
        {
            for(int i=0;i<JointVisuals.Count;++i)
            {
            //Debug.Log("jointsList: "+jointsList[i].gameObject.transform.position);
            JointVisuals[i].SetVector3("jointTransform_position", orderJointsList[i].gameObject.transform.position);
            JointVisuals[i].SetVector3("jointTransform_angles", orderJointsList[i].gameObject.transform.eulerAngles);
            JointVisuals[i].SetVector3("jointTransform_scale", orderJointsList[i].gameObject.transform.localScale);
            //Debug.Log("球"+i+"的坐标位置"+orderJointsList[i].gameObject.transform.position+"特效"+i+"位置"+JointVisuals[i].GetVector3("jointTransform_position"));
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
    if(jointsList.Count==8)
    {
     foreach (string targetName in targetNames)
        {
            for (int i = 0; i < jointsList.Count; i++)
            {
                if (jointsList[i].name == targetName)
                {
                    orderJointsList.Add(jointsList[i]); 
                    
                }
            }
        }
      jointsList.Clear(); 
      attachParticles();
    }
    
    }        
    }
}
