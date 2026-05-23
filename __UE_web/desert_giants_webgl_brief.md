# ТЗ: Desert Giants — Interactive WebGL Scene
## vimark.art / scenes/desert-giants/

---

## 1. Общая концепция

Интерактивная 3D-сцена на базе Three.js, встраиваемая на сайт-портфолио vimark.art.  
Пользователь может вращать камеру вокруг сцены, приближать/отдалять, наблюдать procedural песчаную бурю и динамическое освещение.

**Стиль:** тёмный, кинематографический, золотой акцент `#c9a96e`.  
**Настроение:** тёплый пустынный закат, масштаб, эпика.

---

## 2. Ассеты (файлы)

| Файл | Тип | Размер | Назначение |
|------|-----|--------|------------|
| `desert_scene.glb` | glTF Binary | ~12 MB | Пустыня + 1 центральный гигант + 2 пастуха |
| `giant_billboard_01.png` | PNG (RGBA) | ~100–300 KB | Дальний гигант слева, силуэт с alpha |
| `giant_billboard_02.png` | PNG (RGBA) | ~100–300 KB | Дальний гигант справа, силуэт с alpha |
| `desert_sunset_2k.hdr` | HDR (Radiance) | ~2–4 MB | HDRI освещение из UE5 (2048×1024) |

**Все файлы лежат в:** `scenes/desert-giants/assets/`

---

## 3. Структура GLB (цветокоррекция в коде)

Houdini экспортировал материалы без цвета (серые). Необходимо перекрасить меши **после загрузки GLB** по bounding box / имени.

| Объект | Как определить | Base Color | Roughness | envMapIntensity |
|--------|---------------|------------|-----------|-----------------|
| **Пустыня** | `size.x > 50` или `size.z > 50` | `#C9A96E` | 0.9 | 0.5 |
| **Гигант** | `size.y > 5` | `#8B7355` | 0.65 | 1.2 |
| **Пастухи** | `size.y < 2` | `#4A4035` | 0.8 | 0.8 |

**Код-фрагмент (обязателен):**
```javascript
gltf.scene.traverse((child) => {
    if (child.isMesh && child.material) {
        child.castShadow = true;
        child.receiveShadow = true;

        const box = new THREE.Box3().setFromObject(child);
        const size = box.getSize(new THREE.Vector3());

        if (size.x > 50 || size.z > 50) {
            // Пустыня
            child.material.color.set(0xC9A96E);
            child.material.roughness = 0.9;
            child.material.envMapIntensity = 0.5;
        } else if (size.y > 5) {
            // Гигант
            child.material.color.set(0x8B7355);
            child.material.roughness = 0.65;
            child.material.envMapIntensity = 1.2;
        } else if (size.y < 2) {
            // Пастухи
            child.material.color.set(0x4A4035);
            child.material.roughness = 0.8;
            child.material.envMapIntensity = 0.8;
        }
    }
});
```

---

## 4. Billboard'ы (дальние гиганты)

Два дальних гиганта — это **Sprite** (не Plane), чтобы всегда смотрели в камеру.

| Параметр | Значение |
|----------|----------|
| Тип | `THREE.Sprite` |
| Материал | `SpriteMaterial`, `transparent: true`, `alphaTest: 0.5` |
| Позиция 1 | `(-40, 4, -30)` |
| Позиция 2 | `(50, 4, -25)` |
| Scale | `(8, 10, 1)` — ширина × высота |
| Цвет материала | `0xffffff` (белый, не тонировать) |

**Код-фрагмент:**
```javascript
const billboardTex = new THREE.TextureLoader().load('assets/giant_billboard_01.png');
const billboardMat = new THREE.SpriteMaterial({
    map: billboardTex,
    transparent: true,
    alphaTest: 0.5
});

const sprite1 = new THREE.Sprite(billboardMat);
sprite1.position.set(-40, 4, -30);
sprite1.scale.set(8, 10, 1);
scene.add(sprite1);

// sprite2 — аналогично, с giant_billboard_02.png
const sprite2 = new THREE.Sprite(billboardMat.clone());
sprite2.position.set(50, 4, -25);
sprite2.scale.set(8, 10, 1);
scene.add(sprite2);
```

---

## 5. HDRI / Environment

| Параметр | Значение |
|----------|----------|
| Файл | `assets/desert_sunset_2k.hdr` |
| Загрузчик | `RGBELoader` |
| Mapping | `EquirectangularReflectionMapping` |
| Назначение | `scene.environment` (только IBL, не фон) |
| Фон сцены | `null` (использовать CSS-градиент) |

**Код-фрагмент:**
```javascript
new RGBELoader().load('assets/desert_sunset_2k.hdr', (texture) => {
    texture.mapping = THREE.EquirectangularReflectionMapping;
    scene.environment = texture;
    // scene.background = null; // CSS делает фон
});
```

---

## 6. CSS-фон (вместо HDR-неба)

```css
#canvas-container {
    background: linear-gradient(to bottom, #3d3020 0%, #1f1810 40%, #0f0c09 100%);
}
```

---

## 7. Песчаная буря (procedural, без текстур)

### 7.1. Ground Fog — 5 плоскостей с шейдером

**Vertex Shader:**
```glsl
varying vec2 vUv;
void main() {
    vUv = uv;
    gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0);
}
```

**Fragment Shader:**
```glsl
varying vec2 vUv;
uniform float uTime;
uniform vec3 uColor;
uniform float uOpacity;

// Simplex 2D noise
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
    uv.x += uTime * 0.15;
    uv.y += uTime * 0.03;
    float n = fbm(uv);
    float mask = smoothstep(0.2, 0.6, n * 0.5 + 0.5);
    float edgeFade = smoothstep(0.0, 0.2, vUv.x) * smoothstep(1.0, 0.8, vUv.x)
                   * smoothstep(0.0, 0.2, vUv.y) * smoothstep(1.0, 0.8, vUv.y);
    float alpha = mask * edgeFade * uOpacity;
    gl_FragColor = vec4(uColor, alpha);
}
```

**Uniforms:**
- `uTime`: elapsed time
- `uColor`: `vec3(0.788, 0.663, 0.431)` (=`#C9A96E` в float)
- `uOpacity`: 0.12–0.25 (разное для каждой плоскости)

**Настройки плоскостей:**
- Geometry: `PlaneGeometry(40, 8)`
- Position: Y = 0.3–2.0, Z = -5 до +10
- Material: `ShaderMaterial`, `transparent: true`, `depthWrite: false`, `side: DoubleSide`

### 7.2. Floating Particles — 1200 точек

- `PointsMaterial`, `size: 0.12`
- `CanvasTexture` (radial gradient 64×64)
- `AdditiveBlending`, `color: #c9a96e`
- Bounds: X ±15, Y 0–5, Z ±10
- Wind drift: +X, reset loop

### 7.3. CSS Overlay

```css
#dust-overlay {
    position: absolute; inset: 0;
    pointer-events: none; opacity: 0.06;
    mix-blend-mode: overlay;
    background:
        radial-gradient(circle at 20% 50%, rgba(201,169,110,0.15) 0%, transparent 50%),
        radial-gradient(circle at 80% 20%, rgba(201,169,110,0.1) 0%, transparent 40%);
    animation: dustShift 12s ease-in-out infinite;
}
@keyframes dustShift {
    0%, 100% { transform: translate(0, 0); }
    33% { transform: translate(30px, -10px); }
    66% { transform: translate(-20px, 15px); }
}
```

---

## 8. Камера и управление

| Параметр | Значение |
|----------|----------|
| **Start Position** | `(15, 8, 20)` |
| **Target** | `(0, 4, 0)` — пояс гиганта |
| **Min Distance** | `5` |
| **Max Distance** | `60` |
| **Max Polar Angle** | `Math.PI / 2 - 0.05` (не под землю) |
| **Damping** | `0.05` (плавность) |
| **Auto Rotate** | `false` по умолчанию, кнопка включает `speed: 1.5` |

---

## 9. UI / Оверлей

| Элемент | Стиль |
|---------|-------|
| **Loading screen** | Текст "Loading Scene" + progress bar, цвет `#c9a96e`, фон `#0a0a0a` |
| **Info block** | Верхний левый угол: название сцены, описание, управление |
| **Controls** | Нижний центр: Reset View, Auto Rotate, Back to Portfolio |
| **Кнопки** | `backdrop-filter: blur(10px)`, border `rgba(255,255,255,0.2)`, hover → `#c9a96e` |
| **Шрифт** | `system-ui, sans-serif`, размер 11–12px, `letter-spacing: 0.5px`, uppercase |

---

## 10. Освещение (дополнительно к HDR)

```javascript
const sun = new THREE.DirectionalLight(0xffaa66, 1.5);
sun.position.set(50, 80, 30);
sun.castShadow = true;
sun.shadow.mapSize.set(1024, 1024);
scene.add(sun);

const fill = new THREE.DirectionalLight(0x6688ff, 0.3);
fill.position.set(-30, 20, -30);
scene.add(fill);
```

---

## 11. Производительность / Limits

| Параметр | Лимит |
|----------|-------|
| Pixel Ratio | `Math.min(window.devicePixelRatio, 2)` |
| Shadows | PCFSoft, 1024×1024 |
| Tone Mapping | ACESFilmic, exposure 1.0 |
| Post-processing (Bloom) | **НЕТ** — слишком тяжело для мобильных |
| Fog planes | 5 max |
| Particles | 1200 desktop / 500 mobile |

---

## 12. Структура файлов проекта

```
scenes/desert-giants/
├── index.html
├── main.js
├── style.css
└── assets/
    ├── desert_scene.glb
    ├── giant_billboard_01.png
    ├── giant_billboard_02.png
    └── desert_sunset_2k.hdr
```

---

## 13. Примечания для разработчика (Kimi Code)

- GLB экспортирован из Houdini, материалы серые — **обязательна цветокоррекция в коде** (раздел 3).
- Billboard'ы — PNG с чистым alpha, подготовлены в Photoshop.
- HDR — 2K, warm golden sunset, blur в UE5 не нужен (если уже мягкий).
- Пыль — полностью procedural, никаких PNG-текстур не требуется.
- Все цвета сайта привязаны к акценту `#c9a96e`.
- На мобильном уменьшить particles до 500 и shadow map до 512×512.

---

*Подготовлено: 2026-05-23*  
*Автор: Max Mitenkov (vimark.art)*
