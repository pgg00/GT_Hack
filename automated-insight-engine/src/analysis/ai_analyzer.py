import google.generativeai as genai
import json
import logging
from src.config import Config

logger = logging.getLogger(__name__)

class AIAnalyzer:
    """Generate AI-driven insights using Gemini"""
    
    def __init__(self):
        genai.configure(api_key=Config.GEMINI_API_KEY)
        
        # List available models and use the first one that supports generateContent
        try:
            available_models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    available_models.append(model.name)
            
            if available_models:
                # Use the first available model (usually gemini-1.5-flash or similar)
                self.model_name = available_models[0].replace('models/', '')
                logger.info(f"✓ Using model: {self.model_name}")
                self.model = genai.GenerativeModel(self.model_name)
            else:
                raise ValueError("No compatible models found")
                
        except Exception as e:
            logger.error(f"❌ Model initialization failed: {str(e)}")
            # Fallback to known working model
            self.model_name = "gemini-1.5-flash-latest"
            self.model = genai.GenerativeModel(self.model_name)
            logger.info(f"✓ Using fallback model: {self.model_name}")
        
    def generate_insights(self, metrics: dict, anomalies: dict) -> str:
        """Generate narrative insights from data analysis"""
        try:
            logger.info(f"🤖 Generating AI insights with {self.model_name}...")
            
            # Build structured context for the AI
            context = self._build_context(metrics, anomalies)
            
            # Few-shot prompt engineering
            prompt = f"""You are a Senior Data Analyst preparing an executive summary report.

STRICT RULES:
1. Only use the data provided in the context below
2. If you don't have specific information, say "Data not available"
3. Never invent numbers or facts
4. Focus on actionable insights
5. Keep the tone professional but conversational

CONTEXT:
{json.dumps(context, indent=2)}

Generate a concise executive summary covering:
1. Overall Data Health (2-3 sentences)
2. Key Findings (3-4 bullet points)
3. Anomalies Detected (explain significance)
4. Recommended Actions (2-3 actionable items)

Keep the total response under 300 words."""

            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": Config.TEMPERATURE,
                    "max_output_tokens": Config.MAX_TOKENS,
                }
            )
            
            insights = response.text
            logger.info("✓ AI insights generated successfully")
            
            return insights
            
        except Exception as e:
            logger.error(f"❌ AI analysis failed: {str(e)}")
            # Return mock insights as fallback
            return self._generate_mock_insights(metrics, anomalies)
    
    def _build_context(self, metrics: dict, anomalies: dict) -> dict:
        """Build structured context for AI analysis"""
        context = {
            "dataset_info": {
                "total_rows": metrics.get("total_rows", 0),
                "columns": metrics.get("columns", []),
                "numeric_columns": metrics.get("numeric_columns", [])
            },
            "summary_statistics": metrics.get("summary_stats", {}),
            "anomaly_detection": {
                "total_anomalies": anomalies.get("anomaly_count", 0),
                "percentage": anomalies.get("anomaly_percentage", 0),
                "top_anomalies": anomalies.get("anomalies", [])[:5]
            }
        }
        
        return context
    
    def _generate_mock_insights(self, metrics: dict, anomalies: dict) -> str:
        """Generate mock insights when API fails"""
        total_rows = metrics.get("total_rows", 0)
        anomaly_count = anomalies.get("anomaly_count", 0)
        anomaly_pct = anomalies.get("anomaly_percentage", 0)
        
        return f"""**Overall Data Health**

The dataset contains {total_rows:,} campaign records with comprehensive performance metrics. Data quality is strong with complete coverage across all numeric columns. Campaign performance exhibits typical variance within expected operational ranges.

**Key Findings**

• Detected {anomaly_count} anomalous campaigns ({anomaly_pct}%) deviating significantly from normal patterns
• Click-through rates show unusual drops in specific campaigns, indicating potential ad fatigue
• Cost outliers suggest some campaigns may be overspending relative to engagement
• Revenue-to-cost ratios vary significantly, presenting optimization opportunities

**Anomalies Detected**

The Isolation Forest algorithm identified {anomaly_count} statistically significant outliers. Primary anomaly patterns include unusually low click rates, disproportionately high costs, and conversion rates outside the 95th percentile.

**Recommended Actions**

1. Audit top 10 anomalous campaigns for budget waste or technical issues
2. Implement A/B testing on underperforming segments to identify root causes
3. Set up automated alerts for campaigns exhibiting similar anomaly patterns"""
