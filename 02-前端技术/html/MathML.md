# MathML

## 使用示例

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>数学之美 - MathML展示</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: 'Segoe UI', 'Microsoft YaHei', sans-serif;
        }
        
        body {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #333;
        }
        
        .container {
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 40px;
            position: relative;
            overflow: hidden;
        }
        
        .container::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 5px;
            background: linear-gradient(90deg, #667eea, #764ba2);
        }
        
        header {
            text-align: center;
            margin-bottom: 40px;
        }
        
        h1 {
            color: #2c3e50;
            margin-bottom: 10px;
            font-weight: 600;
            font-size: 2.5rem;
        }
        
        .subtitle {
            color: #7f8c8d;
            font-size: 1.2rem;
        }
        
        .intro {
            background: #f8f9fa;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 30px;
            line-height: 1.6;
            font-size: 1.1rem;
            border-left: 4px solid #667eea;
        }
        
        .formula-section {
            margin-bottom: 50px;
        }
        
        .section-title {
            color: #3498db;
            border-bottom: 2px solid #3498db;
            padding-bottom: 12px;
            margin-bottom: 25px;
            font-size: 1.8rem;
        }
        
        .formula-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 25px;
        }
        
        .formula-card {
            background: #f8f9fa;
            border-radius: 12px;
            padding: 25px;
            transition: transform 0.3s, box-shadow 0.3s;
            border: 1px solid #e9ecef;
        }
        
        .formula-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
        }
        
        .formula-label {
            font-weight: bold;
            margin-bottom: 15px;
            color: #2c3e50;
            font-size: 1.1rem;
            text-align: center;
        }
        
        .formula {
            font-size: 1.2rem;
            padding: 20px;
            background: white;
            border-radius: 8px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            min-height: 80px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .footer {
            text-align: center;
            margin-top: 40px;
            color: #7f8c8d;
            font-size: 0.9rem;
            padding-top: 20px;
            border-top: 1px solid #e9ecef;
        }
        
        .math-highlight {
            color: #e74c3c;
            font-weight: bold;
        }
        
        @media (max-width: 768px) {
            .container {
                padding: 20px;
            }
            
            h1 {
                font-size: 2rem;
            }
            
            .formula-grid {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>数学之美</h1>
            <p class="subtitle">MathML 数学公式展示</p>
        </header>
        
        <div class="intro">
            <p>数学是科学的语言，是理解世界的钥匙。下面展示了一些经典的数学公式，它们使用MathML标记语言呈现，展现了数学的优雅与精确。</p>
        </div>
        
        <div class="formula-section">
            <h2 class="section-title">代数与算术</h2>
            
            <div class="formula-grid">
                <div class="formula-card">
                    <div class="formula-label">二次方程求根公式</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <mi>x</mi>
                            <mo>=</mo>
                            <mfrac>
                                <mrow>
                                    <mo>-</mo>
                                    <mi>b</mi>
                                    <mo>±</mo>
                                    <msqrt>
                                        <msup>
                                            <mi>b</mi>
                                            <mn>2</mn>
                                        </msup>
                                        <mo>-</mo>
                                        <mn>4</mn>
                                        <mi>a</mi>
                                        <mi>c</mi>
                                    </msqrt>
                                </mrow>
                                <mrow>
                                    <mn>2</mn>
                                    <mi>a</mi>
                                </mrow>
                            </mfrac>
                        </math>
                    </div>
                </div>
                
                <div class="formula-card">
                    <div class="formula-label">勾股定理</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <msup>
                                <mi>a</mi>
                                <mn>2</mn>
                            </msup>
                            <mo>+</mo>
                            <msup>
                                <mi>b</mi>
                                <mn>2</mn>
                            </msup>
                            <mo>=</mo>
                            <msup>
                                <mi>c</mi>
                                <mn>2</mn>
                            </msup>
                        </math>
                    </div>
                </div>
                
                <div class="formula-card">
                    <div class="formula-label">二项式定理</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <msup>
                                <mrow>
                                    <mo>(</mo>
                                    <mi>a</mi>
                                    <mo>+</mo>
                                    <mi>b</mi>
                                    <mo>)</mo>
                                </mrow>
                                <mi>n</mi>
                            </msup>
                            <mo>=</mo>
                            <munderover>
                                <mo>∑</mo>
                                <mrow>
                                    <mi>k</mi>
                                    <mo>=</mo>
                                    <mn>0</mn>
                                </mrow>
                                <mi>n</mi>
                            </munderover>
                            <mrow>
                                <mo>(</mo>
                                <mfrac linethickness="0">
                                    <mi>n</mi>
                                    <mi>k</mi>
                                </mfrac>
                                <mo>)</mo>
                            </mrow>
                            <msup>
                                <mi>a</mi>
                                <mrow>
                                    <mi>n</mi>
                                    <mo>-</mo>
                                    <mi>k</mi>
                                </mrow>
                            </msup>
                            <msup>
                                <mi>b</mi>
                                <mi>k</mi>
                            </msup>
                        </math>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="formula-section">
            <h2 class="section-title">微积分</h2>
            
            <div class="formula-grid">
                <div class="formula-card">
                    <div class="formula-label">牛顿-莱布尼茨公式</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <msubsup>
                                <mo>∫</mo>
                                <mi>a</mi>
                                <mi>b</mi>
                            </msubsup>
                            <mi>f</mi>
                            <mo>(</mo>
                            <mi>x</mi>
                            <mo>)</mo>
                            <mi>d</mi>
                            <mi>x</mi>
                            <mo>=</mo>
                            <mi>F</mi>
                            <mo>(</mo>
                            <mi>b</mi>
                            <mo>)</mo>
                            <mo>-</mo>
                            <mi>F</mi>
                            <mo>(</mo>
                            <mi>a</mi>
                            <mo>)</mo>
                        </math>
                    </div>
                </div>
                
                <div class="formula-card">
                    <div class="formula-label">导数定义</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <msup>
                                <mi>f</mi>
                                <mo>′</mo>
                            </msup>
                            <mo>(</mo>
                            <mi>x</mi>
                            <mo>)</mo>
                            <mo>=</mo>
                            <munder>
                                <mo>lim</mo>
                                <mrow>
                                    <mi>h</mi>
                                    <mo>→</mo>
                                    <mn>0</mn>
                                </mrow>
                            </munder>
                            <mfrac>
                                <mrow>
                                    <mi>f</mi>
                                    <mo>(</mo>
                                    <mi>x</mi>
                                    <mo>+</mo>
                                    <mi>h</mi>
                                    <mo>)</mo>
                                    <mo>-</mo>
                                    <mi>f</mi>
                                    <mo>(</mo>
                                    <mi>x</mi>
                                    <mo>)</mo>
                                </mrow>
                                <mi>h</mi>
                            </mfrac>
                        </math>
                    </div>
                </div>
                
                <div class="formula-card">
                    <div class="formula-label">泰勒展开</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <mi>f</mi>
                            <mo>(</mo>
                            <mi>x</mi>
                            <mo>)</mo>
                            <mo>=</mo>
                            <munderover>
                                <mo>∑</mo>
                                <mrow>
                                    <mi>n</mi>
                                    <mo>=</mo>
                                    <mn>0</mn>
                                </mrow>
                                <mi>∞</mi>
                            </munderover>
                            <mfrac>
                                <mrow>
                                    <msup>
                                        <mi>f</mi>
                                        <mrow>
                                            <mo>(</mo>
                                            <mi>n</mi>
                                            <mo>)</mo>
                                        </mrow>
                                    </msup>
                                    <mo>(</mo>
                                    <mi>a</mi>
                                    <mo>)</mo>
                                </mrow>
                                <mrow>
                                    <mi>n</mi>
                                    <mo>!</mo>
                                </mrow>
                            </mfrac>
                            <msup>
                                <mrow>
                                    <mo>(</mo>
                                    <mi>x</mi>
                                    <mo>-</mo>
                                    <mi>a</mi>
                                    <mo>)</mo>
                                </mrow>
                                <mi>n</mi>
                            </msup>
                        </math>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="formula-section">
            <h2 class="section-title">几何与三角</h2>
            
            <div class="formula-grid">
                <div class="formula-card">
                    <div class="formula-label">圆的面积</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <mi>A</mi>
                            <mo>=</mo>
                            <mi>π</mi>
                            <msup>
                                <mi>r</mi>
                                <mn>2</mn>
                            </msup>
                        </math>
                    </div>
                </div>
                
                <div class="formula-card">
                    <div class="formula-label">欧拉公式</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <msup>
                                <mi>e</mi>
                                <mrow>
                                    <mi>i</mi>
                                    <mi>θ</mi>
                                </mrow>
                            </msup>
                            <mo>=</mo>
                            <mi>cos</mi>
                            <mi>θ</mi>
                            <mo>+</mo>
                            <mi>i</mi>
                            <mi>sin</mi>
                            <mi>θ</mi>
                        </math>
                    </div>
                </div>
                
                <div class="formula-card">
                    <div class="formula-label">球体体积</div>
                    <div class="formula">
                        <math xmlns="http://www.w3.org/1998/Math/MathML">
                            <mi>V</mi>
                            <mo>=</mo>
                            <mfrac>
                                <mn>4</mn>
                                <mn>3</mn>
                            </mfrac>
                            <mi>π</mi>
                            <msup>
                                <mi>r</mi>
                                <mn>3</mn>
                            </msup>
                        </math>
                    </div>
                </div>
            </div>
        </div>
        
        <div class="footer">
            <p>探索数学之美，发现宇宙的奥秘</p>
        </div>
    </div>
</body>
</html>
```
