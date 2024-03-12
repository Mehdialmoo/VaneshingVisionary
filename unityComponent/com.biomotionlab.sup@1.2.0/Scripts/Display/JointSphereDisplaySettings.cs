using System;
using log4net.Filter;
using UnityEngine;

// ReSharper disable InconsistentNaming

namespace Display {
    
    [Serializable]
    public class JointSphereDisplaySettings {
       
        public float PointLightDisplaySize = 10.0f;
        public bool DrawSidesDifferentColors;
        public Material LeftSideMaterial;
        public Material RightSideMaterial;
    }
}