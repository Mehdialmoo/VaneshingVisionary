using System;
using System.Collections.Generic;
using FileLoaders;
using Playback;
using Display;
using Settings;
using SMPLModel;
using UnityEngine;
using UnityEngine.VFX;

namespace yoga{
public class AnimationManager : MonoBehaviour {
    
    
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

    void Update() {
    attachParticles();
    //PythonTest.GetFailedScore+=setFailedParam;
    if(nCharacter != null)
    {
    meshVisual.SetVector3("MeshTransform_position", Pelvis.position);
     meshVisual.SetVector3("MeshTransform_angles", Pelvis.eulerAngles);
     meshVisual.SetVector3("MeshTransform_scale", Pelvis.localScale);
     //Debug.Log("jointsList.Count"+jointsList.Count);
     //Debug.Log("nCharacter: " + (nCharacter != null ? nCharacter.name : "null"));
    }
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
    //  for(int i=times*8;i<JointVisuals.Count;++i)
    //  {
    //  JointVisuals[i].SetVector3("jointTransform_position", jointsList[i].gameObject.transform.position);
    //  JointVisuals[i].SetVector3("jointTransform_angles", jointsList[i].gameObject.transform.eulerAngles);
    //  JointVisuals[i].SetVector3("jointTransform_scale", jointsList[i].gameObject.transform.localScale);
    //  }
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
        // 使用character对象进行操作
    }
    void ParticleCorrect(JointSphere jSphere)
    {
        //应该在第二个被初始化的时候
        if(jSphere.isMark==true)
        {
            jointsList.Add(jSphere);
            
        }
        
    }
    void setFailedParam(float failedScore,int position)
    {
        //Debug.Log("failedScore : "+ failedScore+"failedPosition"+position);

    }
}

}
