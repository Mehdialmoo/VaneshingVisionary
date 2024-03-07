using System.Collections;
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
namespace yoga{
public class PythonTest : MonoBehaviour
{
    [SerializeField] AnimationListAsset animationListAsset;
    [SerializeField] PlaybackSettings playbackSettings = default;
    [SerializeField] BodySettings bodySettings;
    [SerializeField] DisplaySettings displaySettings;
    [SerializeField] VisualEffect meshVisual;
    //[SerializeField] VisualEffect JointVisual;
    List<List<AMASSAnimation>> animations;
    SUPPlayer player;
    GameObject nCharacter;
    int times = 0;
    Transform Pelvis;
    int currentlyPlayingIndex = 0;
    List<JointSphere> jointsList = new List<JointSphere>();
    public List<VisualEffect> JointVisuals=new List<VisualEffect>();

    List<float> numbers = new List<float>();
    //public static event Action <float,int> GetFailedScore;
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
    void OnEnable()
    {
        player = new SUPPlayer(playbackSettings, displaySettings, bodySettings);
        // load animations from list asset
        SUPLoader.LoadFromListAssetAsync(animationListAsset, DoneLoading);
        ModelDefinition.OnCharacterInstantiated += HandleCharacterInstantiated;
        PointLightDisplay.ParticleAction+=ParticleCorrect;
       
    }

    void DoneLoading(List<List<AMASSAnimation>> loadedAnimations) {
        
        // save loaded animations to memory
        this.animations = loadedAnimations;
        Debug.Log("animation Size:"+animations.Count);
        // Start playing first animation when loading complete
        player.Play(animations[0]);
        
    }
    void Start()
    {
        udpSocket = FindObjectOfType<UdpSocket>();
        
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
                                    //TODO:GetFailedScore?.Invoke(numbers[i],i);
                                    Debug.Log("传走的数值是多少: "+numbers[i]);
                                    Debug.Log("传走的index是多少: "+i);
                                    JointVisuals[i].SetFloat("particleSize",numbers[i]*0.1f);
                                    JointVisuals[i].SetVector3("colorControl",new Vector3(1.0f,0.0f,0.0f));
                                }
                        }
                numbers.Clear();
                }
            }
        }
    }
    void Update()
    { 
    SearchValue();
    attachParticles();
    meshAttach();   
      if (Input.GetKeyDown(KeyCode.Space)) {
            times++;
            
            // Stop currently playing animation
            player.StopCurrentAnimations();
            
            // Increment our animation index
            currentlyPlayingIndex++;
            
            // If reached end, restart all.
            if (currentlyPlayingIndex >= animations.Count) currentlyPlayingIndex = 0;
           
            // Play the next animation
            player.Play(animations[currentlyPlayingIndex]);
        } 
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
        if(jointsList.Count==8)
        {
            for(int i=0;i<JointVisuals.Count;++i)
            {
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
           
}
}

