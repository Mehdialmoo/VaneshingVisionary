using SMPLModel;
using UnityEngine;
using UnityEngine.Serialization;
using System;
namespace Display {
    
    /// <summary>
    /// This renders point lights (spheres) for the joints of a body.
    /// </summary>
    public class PointLightDisplay : MonoBehaviour {
        public static event Action<JointSphere> ParticleAction;
        SkinnedMeshRenderer meshRenderer;

        [FormerlySerializedAs("PointLightPrefab")] [SerializeField]
        JointSphere jointSpherePrefab = default;

        SMPLCharacter smplCharacter;
        public bool DisplayPointLights => smplCharacter.DisplaySettings.DisplayPointLights == PointLightDisplayState.On;

        GameObject pointLightContainer;
        public GameObject[] jointSpheres;

        void OnEnable() {
            smplCharacter = GetComponent<SMPLCharacter>();
            if (meshRenderer == null) meshRenderer = GetComponentInChildren<SkinnedMeshRenderer>();
            if (pointLightContainer == null) {
                SetupPointLights();
            }
        }

        void SetupPointLights() {
            pointLightContainer = new GameObject {name = "JointSphere Container"};
            pointLightContainer.transform.parent = transform;
            CreatePointLightsInBoneHierarchy(meshRenderer.bones[0]);
        }

        /// <summary>
        /// Walks down Bone Hierarchy to create linked point lights
        /// </summary>
        /// <param name="parent"></param>
        void CreatePointLightsInBoneHierarchy(Transform parent) {
            JointSphere newJointSphere = Instantiate(jointSpherePrefab, pointLightContainer.transform);
            newJointSphere.AttachBone(smplCharacter, this, parent);
            if(newJointSphere.linkedBone.name=="R_Hip"||newJointSphere.linkedBone.gameObject.name=="L_Hip"||newJointSphere.linkedBone.gameObject.name=="R_Shoulder"
            ||newJointSphere.linkedBone.gameObject.name=="L_Shoulder"||newJointSphere.linkedBone.gameObject.name=="R_Knee"||newJointSphere.linkedBone.gameObject.name=="L_Knee"||
            newJointSphere.linkedBone.gameObject.name=="L_Elbow"||newJointSphere.linkedBone.gameObject.name=="R_Elbow")
            {
                newJointSphere.isMark=true;
            }
            ParticleAction?.Invoke(newJointSphere);
            foreach (Transform child in parent) {
                if (Bones.IsBone(child)) {
                    CreatePointLightsInBoneHierarchy(child);
                }
            }
        }
//TODO:not sure here.
        void OnDisable() {
            DestroyImmediate(pointLightContainer);
           
        }
    }
    
}
