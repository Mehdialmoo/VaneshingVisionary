using System;
using SMPLModel;
using UnityEngine;

// ReSharper disable ParameterHidesMember

namespace Display {
    
    /// <summary>
    /// A single point light for displaying a joint's location.
    /// </summary>
    [ExecuteInEditMode]
    public class JointSphere : MonoBehaviour {
        

        [SerializeField]
        JointSphereDisplaySettings defaultPointlightDisplaySettings = default;

        JointSphereDisplaySettings Settings {
            get {
                if (smplCharacter != null && smplCharacter.DisplaySettings != null) {
                    return smplCharacter.DisplaySettings.jointSphereDisplaySettings;
                }
                return defaultPointlightDisplaySettings;
            }
        }
        public Transform linkedBone;
        public MeshRenderer meshRenderer;
        PointLightDisplay pointLightDisplay;
        SMPLCharacter smplCharacter;
        public bool isMark = false;
        void OnEnable() {
            meshRenderer = GetComponent<MeshRenderer>();
        }
        
        public void AttachBone(SMPLCharacter smplCharacter, PointLightDisplay pointLightDisplay, 
                               Transform bone) {
            this.smplCharacter = smplCharacter;
            linkedBone = bone;
            this.pointLightDisplay = pointLightDisplay;
            name = $"JointSphere for {bone.name}";
            var cachedTransform = transform;
            cachedTransform.localPosition = Vector3.zero;
            cachedTransform.localScale = new Vector3(Settings.PointLightDisplaySize,
                                             Settings.PointLightDisplaySize,
                                             Settings.PointLightDisplaySize);
            
        }

        void LateUpdate() {
            
            
            this.transform.localScale = new Vector3(Settings.PointLightDisplaySize, Settings.PointLightDisplaySize,
            Settings.PointLightDisplaySize);
            //TODO:check the linkbone and set the renderer.
            if (linkedBone != null) {
            //Debug.Log("linked bones:"+linkedBone.gameObject.name);
            transform.position = linkedBone.position;
            if(linkedBone.gameObject.name=="R_Hip"||linkedBone.gameObject.name=="L_Hip"||linkedBone.gameObject.name=="R_Shoulder"
            ||linkedBone.gameObject.name=="L_Shoulder"||linkedBone.gameObject.name=="R_Knee"||linkedBone.gameObject.name=="L_Knee"||
            linkedBone.gameObject.name=="L_Elbow"||linkedBone.gameObject.name=="R_Elbow")
                {
                meshRenderer.enabled = pointLightDisplay.DisplayPointLights;
               
                }

            //     //Debug.Log("meshRender enable: "+meshRenderer.enabled);
            // }
            // else {
            
            //     meshRenderer.enabled = false;
            }
            
        }


        
    }
}