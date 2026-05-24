import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { RGBELoader } from 'three/addons/loaders/RGBELoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

/* =========================================================
   CONFIG
   ========================================================= */
const ACCENT = 0xc9a96e;
const IS_MOBILE = window.innerWidth < 768 || window.matchMedia('(pointer: coarse)').matches;
const PARTICLE_COUNT = IS_MOBILE ? 500 : 1200;
const SHADOW_MAP_SIZE = IS_MOBILE ? 512 : 1024;

/* =========================================================
   SCENE SETUP
   ========================================================= */
const container = document.getElementById('canvas-container');

const scene = new THREE.Scene();
scene.background = null;

const camera = new THREE.PerspectiveCamera(
    75,
    window.innerWidth / window.innerHeight,
    0.1,
    300
);
camera.position.set(-55, 1.2, 12);

const renderer = new THREE.WebGLRenderer({ antialias: true, alpha: true });
renderer.setSize(window.innerWidth, window.innerHeight);
renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
renderer.toneMapping = THREE.ACESFilmicToneMapping;
renderer.toneMappingExposure = 1.0;
renderer.shadowMap.enabled = true;
renderer.shadowMap.type = THREE.PCFSoftShadowMap;
container.appendChild(renderer.domElement);

const controls = new OrbitControls(camera, renderer.domElement);
controls.target.set(0, 4, 0);
controls.enableDamping = true;
controls.dampingFactor = 0.05;
controls.minDistance = 5;
controls.maxDistance = 80;
controls.maxPolarAngle = Math.PI / 2 - 0.05;
controls.autoRotate = false;
controls.autoRotateSpeed = 1.5;

/* =========================================================
   LOADING MANAGER
   ========================================================= */
const loadingScreen = document.getElementById('loading-screen');
const loadingBarFill = document.querySelector('.loading-bar-fill');
const loadingError = document.getElementById('loading-error');

function showLoadingError(msg) {
    if (loadingError) {
        loadingError.textContent = msg;
        loadingError.classList.add('visible');
    }
}

if (window.location.protocol === 'file:') {
    showLoadingError('Open via local server required:\npython3 -m http.server 8080');
}

const manager = new THREE.LoadingManager();

manager.onProgress = (url, itemsLoaded, itemsTotal) => {
    const progress = (itemsLoaded / itemsTotal) * 100;
    loadingBarFill.style.width = `${progress}%`;
};

manager.onLoad = () => {
    loadingBarFill.style.width = '100%';
    setTimeout(() => {
        loadingScreen.classList.add('hidden');
    }, 400);
};

manager.onError = (url) => {
    console.error('[Load error]', url);
    showLoadingError('Failed to load: ' + url.split('/').pop());
};

setTimeout(() => {
    if (!loadingScreen.classList.contains('hidden')) {
        loadingBarFill.style.width = '100%';
        loadingScreen.classList.add('hidden');
    }
}, 15000);

/* =========================================================
   LIGHTING
   ========================================================= */
const sun = new THREE.DirectionalLight(0xffcc88, 3.0);
sun.position.set(-60, 25, 40);
sun.castShadow = true;
sun.shadow.mapSize.set(SHADOW_MAP_SIZE, SHADOW_MAP_SIZE);
sun.shadow.camera.near = 0.5;
sun.shadow.camera.far = 200;
sun.shadow.camera.left = -60;
sun.shadow.camera.right = 60;
sun.shadow.camera.top = 60;
sun.shadow.camera.bottom = -60;
scene.add(sun);

const fill = new THREE.DirectionalLight(0x6688ff, 0.15);
fill.position.set(30, 20, -30);
scene.add(fill);

const ambient = new THREE.AmbientLight(0x5a4a35, 0.5);
scene.add(ambient);

/* =========================================================
   ASSET LOADING
   ========================================================= */
const gltfLoader = new GLTFLoader(manager);
const rgbeLoader = new RGBELoader(manager);
const texLoader = new THREE.TextureLoader(manager);

// HDR Environment
rgbeLoader.load('assets/desert_sunset_2k.hdr',
    (texture) => {
        texture.mapping = THREE.EquirectangularReflectionMapping;
        scene.environment = texture;
    },
    undefined,
    (err) => console.error('HDR load error:', err)
);

// GLB Scene
gltfLoader.load('assets/desert_scene.glb',
    (gltf) => {
        let desertMesh = null;
        let desertMaterial = null;

        gltf.scene.traverse((child) => {
            if (child.isMesh && child.material) {
                child.castShadow = true;
                child.receiveShadow = true;
                const box = new THREE.Box3().setFromObject(child);
                const size = box.getSize(new THREE.Vector3());
                const center = box.getCenter(new THREE.Vector3());
                console.log('MESH:', child.name, 'size:', size.x.toFixed(1), size.y.toFixed(1), size.z.toFixed(1), 'center:', center.x.toFixed(1), center.y.toFixed(1), center.z.toFixed(1), 'verts:', child.geometry.attributes.position.count);

                // Identify desert mesh: very flat and large in X/Z
                if (size.y < 1.0 && (size.x > 40 || size.z > 40)) {
                    desertMesh = child;
                    desertMaterial = child.material.clone();
                    console.log('Found desert mesh:', child.name);
                }
            }
        });

        // Remove original desert mesh and replace with infinite plane
        if (desertMesh && desertMesh.parent) {
            desertMesh.parent.remove(desertMesh);
            console.log('Removed original desert mesh from scene');
        }

        const sandNormal = texLoader.load('assets/Normal_4K_Rippled_Sand.PNG',
            undefined, undefined, (err) => console.error('Normal map error:', err));
        sandNormal.wrapS = THREE.RepeatWrapping;
        sandNormal.wrapT = THREE.RepeatWrapping;
        sandNormal.repeat.set(120, 120);

        const planeGeo = new THREE.PlaneGeometry(1000, 1000);
        const planeMat = new THREE.MeshStandardMaterial({
            color: 0x5a3d20,
            roughness: 0.95,
            envMapIntensity: 0.4,
            normalMap: sandNormal,
            normalScale: new THREE.Vector2(1.0, 1.0),
        });
        const desertPlane = new THREE.Mesh(planeGeo, planeMat);
        desertPlane.rotation.x = -Math.PI / 2;
        desertPlane.position.y = 0;
        desertPlane.receiveShadow = true;
        scene.add(desertPlane);
        console.log('Added infinite desert plane');

        scene.add(gltf.scene);
    },
    undefined,
    (err) => console.error('GLB load error:', err)
);

/* =========================================================
   GROUND FOG (5 PLANES)
   ========================================================= */
const fogVertexShader = `
varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
`;

const fogFragmentShader = `
varying vec2 vUv;
uniform float uTime;
uniform vec3 uColor;
uniform float uOpacity;

vec3 mod289(vec3 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec2 mod289(vec2 x) { return x - floor(x * (1.0 / 289.0)) * 289.0; }
vec3 permute(vec3 x) { return mod289(((x*34.0)+1.0)*x); }

float snoise(vec2 v) {
    const vec4 C = vec4(0.211324865405187, 0.366025403784439,
                       -0.577350269189626, 0.024390243902439);
    vec2 i  = floor(v + dot(v, C.yy));
    vec2 x0 = v -   i + dot(i, C.xx);
    vec2 i1;
    i1 = (x0.x > x0.y) ? vec2(1.0, 0.0) : vec2(0.0, 1.0);
    vec4 x12 = x0.xyxy + C.xxzz;
    x12.xy -= i1;
    i = mod289(i);
    vec3 p = permute(permute(i.y + vec3(0.0, i1.y, 1.0))
                    + i.x + vec3(0.0, i1.x, 1.0));
    vec3 m = max(0.5 - vec3(dot(x0,x0), dot(x12.xy,x12.xy),
                            dot(x12.zw,x12.zw)), 0.0);
    m = m*m; m = m*m;
    vec3 x = 2.0 * fract(p * C.www) - 1.0;
    vec3 h = abs(x) - 0.5;
    vec3 ox = floor(x + 0.5);
    vec3 a0 = x - ox;
    m *= 1.79284291400159 - 0.85373472095314 * (a0*a0 + h*h);
    vec3 g;
    g.x  = a0.x  * x0.x  + h.x  * x0.y;
    g.yz = a0.yz * x12.xz + h.yz * x12.yw;
    return 130.0 * dot(m, g);
}

float fbm(vec2 p) {
    float value = 0.0;
    float amplitude = 0.5;
    float frequency = 1.0;
    for (int i = 0; i < 4; i++) {
        value += amplitude * snoise(p * frequency);
        frequency *= 2.0;
        amplitude *= 0.5;
    }
    return value;
}

void main() {
    vec2 uv = vUv * 3.0;
    uv.x += uTime * 0.05;
    uv.y += uTime * 0.0;
    float n = fbm(uv);
    float mask = smoothstep(0.2, 0.6, n * 0.5 + 0.5);
    float edgeFade = smoothstep(0.0, 0.2, vUv.x) * smoothstep(1.0, 0.8, vUv.x)
                   * smoothstep(0.0, 0.2, vUv.y) * smoothstep(1.0, 0.8, vUv.y);
    float alpha = mask * edgeFade * uOpacity;
    gl_FragColor = vec4(uColor, alpha);
}
`;

const fogConfigs = [
    { y: -0.10, z: -45, opacity: 0.15 },
    { y: 0.30, z: -25, opacity: 0.15 },
    { y: 0.70, z: -5, opacity: 0.15 },
    { y: 1.10, z: 15, opacity: 0.15 },
    { y: 1.50, z: 35, opacity: 0.15 },
];

const fogUniforms = { value: 0 };

fogConfigs.forEach((cfg) => {
    const geometry = new THREE.PlaneGeometry(120, 120);
    const material = new THREE.ShaderMaterial({
        vertexShader: fogVertexShader,
        fragmentShader: fogFragmentShader,
        uniforms: {
            uTime: fogUniforms,
            uColor: { value: new THREE.Vector3(0.55, 0.45, 0.30) },
            uOpacity: { value: cfg.opacity },
        },
        transparent: true,
        depthWrite: false,
        side: THREE.DoubleSide,
    });
    const mesh = new THREE.Mesh(geometry, material);
    mesh.position.set(0, cfg.y, cfg.z);
    mesh.rotation.x = -Math.PI / 2;
    scene.add(mesh);
});

/* =========================================================
   FLOATING PARTICLES
   ========================================================= */
function createParticleTexture() {
    const canvas = document.createElement('canvas');
    canvas.width = 64;
    canvas.height = 64;
    const ctx = canvas.getContext('2d');
    const grad = ctx.createRadialGradient(32, 32, 0, 32, 32, 32);
    grad.addColorStop(0, 'rgba(255,255,255,1)');
    grad.addColorStop(0.4, 'rgba(255,255,255,0.5)');
    grad.addColorStop(1, 'rgba(255,255,255,0)');
    ctx.fillStyle = grad;
    ctx.fillRect(0, 0, 64, 64);
    const texture = new THREE.CanvasTexture(canvas);
    texture.needsUpdate = true;
    return texture;
}

const particleGeo = new THREE.BufferGeometry();
const particlePositions = new Float32Array(PARTICLE_COUNT * 3);
const particleSpeeds = new Float32Array(PARTICLE_COUNT);

for (let i = 0; i < PARTICLE_COUNT; i++) {
    particlePositions[i * 3] = (Math.random() - 0.5) * 30;
    particlePositions[i * 3 + 1] = Math.random() * 5;
    particlePositions[i * 3 + 2] = (Math.random() - 0.5) * 20;
    particleSpeeds[i] = 0.2 + Math.random() * 0.8;
}

particleGeo.setAttribute('position', new THREE.BufferAttribute(particlePositions, 3));

const particleMat = new THREE.PointsMaterial({
    size: 0.12,
    map: createParticleTexture(),
    transparent: true,
    opacity: 0.8,
    blending: THREE.AdditiveBlending,
    depthWrite: false,
    color: ACCENT,
});

const particles = new THREE.Points(particleGeo, particleMat);
scene.add(particles);

/* =========================================================
   UI CONTROLS
   ========================================================= */
const btnReset = document.getElementById('btn-reset');
const btnAuto = document.getElementById('btn-auto');

btnReset.addEventListener('click', () => {
    camera.position.set(-50, 1.5, 10);
    controls.target.set(-45, 3, 2);
    controls.update();
});

btnAuto.addEventListener('click', () => {
    controls.autoRotate = !controls.autoRotate;
    btnAuto.classList.toggle('active', controls.autoRotate);
});

/* =========================================================
   RESIZE
   ========================================================= */
window.addEventListener('resize', () => {
    camera.aspect = window.innerWidth / window.innerHeight;
    camera.updateProjectionMatrix();
    renderer.setSize(window.innerWidth, window.innerHeight);
});

/* =========================================================
   ANIMATION LOOP
   ========================================================= */
const clock = new THREE.Clock();

function animate() {
    requestAnimationFrame(animate);

    const elapsed = clock.getElapsedTime();
    fogUniforms.value = elapsed;

    const positions = particles.geometry.attributes.position.array;
    for (let i = 0; i < PARTICLE_COUNT; i++) {
        positions[i * 3] += particleSpeeds[i] * 0.015;
        positions[i * 3 + 1] += Math.sin(elapsed * 0.5 + i) * 0.002;
        if (positions[i * 3] > 15) {
            positions[i * 3] = -15;
            positions[i * 3 + 1] = Math.random() * 5;
            positions[i * 3 + 2] = (Math.random() - 0.5) * 20;
        }
    }
    particles.geometry.attributes.position.needsUpdate = true;

    controls.update();
    renderer.render(scene, camera);
}

animate();
