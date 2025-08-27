"""CrewAI agents and task routing"""

import os
from typing import Optional, Dict, Any, List
from crewai import Agent, Task, Crew
from crewai.tools import BaseTool
from pydantic import BaseModel, Field

from .intents import classifier, Intent
from ..domain.services import LicenseService
from ..config import config

# Set OpenAI API key for CrewAI
if config.openai_api_key:
    os.environ["OPENAI_API_KEY"] = config.openai_api_key
else:
    print("⚠️  OPENAI_API_KEY not set in .env file - CrewAI may not work properly")


class LicenseToolInput(BaseModel):
    """Input schema for license tools"""
    instance_id: Optional[str] = Field(None, description="PingFederate instance ID")


class GetLicenseDetailsTool(BaseTool):
    """Tool for retrieving license information"""
    name: str = "get_license_details"
    description: str = "Get license details for PingFederate instances from cache"
    args_schema: type[BaseModel] = LicenseToolInput
    
    def _run(self, instance_id: Optional[str] = None) -> str:
        """Execute license details retrieval"""
        try:
            service = LicenseService()
            
            if instance_id:
                record = service.get_license(instance_id)
                return f"License for {instance_id}: Status={record['status']}, Expires={record['expiry_date'][:10]}, Days={record['days_to_expiry']}"
            else:
                records = service.get_all_licenses()
                if not records:
                    return "No license data found. Run refresh first."
                
                summary = []
                for record in records:
                    summary.append(f"{record['instance_id']}: {record['status']} (expires {record['expiry_date'][:10]})")
                
                return f"License Summary:\n" + "\n".join(summary)
                
        except Exception as e:
            return f"Error retrieving license details: {e}"


class ApplyLicenseTool(BaseTool):
    """Tool for applying license updates"""
    name: str = "apply_license"
    description: str = "Apply new license to a PingFederate instance (requires --file parameter)"
    args_schema: type[BaseModel] = LicenseToolInput
    
    def _run(self, instance_id: Optional[str] = None) -> str:
        """Execute license application"""
        if not instance_id:
            return "Error: Instance ID is required for license application. Use --instance parameter."
        
        return f"License application requires file input. Use: pf-agent license apply --instance {instance_id} --file <path>"


def create_license_getter() -> Agent:
    """Create the license getter agent"""
    return Agent(
        role='License Information Specialist',
        goal='Retrieve and display PingFederate license information in clear, human-readable format',
        backstory='You are an expert in PingFederate license management. You always present information in clear, numbered lists or simple text format - never JSON. You focus on making complex license data easy to understand for operations teams. Remember: licenses expire, not instances.',
        tools=[GetLicenseDetailsTool()],
        verbose=False,
        allow_delegation=False
    )


def create_license_updater() -> Agent:
    """Create the license updater agent"""
    return Agent(
        role='License Update Specialist', 
        goal='Guide users through PingFederate license application processes',
        backstory='You are an expert in PingFederate license updates, helping users apply new licenses safely and efficiently.',
        tools=[ApplyLicenseTool()],
        verbose=False,
        allow_delegation=False
    )


def route_intent(query: str, instance_hint: Optional[str] = None) -> str:
    """Route user query to appropriate CrewAI agent based on intent"""
    
    # Check if OpenAI API key is available
    if not config.openai_api_key:
        print("⚠️  No OpenAI API key found. Falling back to direct service call...")
        service = LicenseService()
        
        try:
            if instance_hint:
                record = service.get_license(instance_hint)
                return f"License for {instance_hint}: Status={record['status']}, Expires={record['expiry_date'][:10]}, Days={record['days_to_expiry']}"
            else:
                records = service.get_all_licenses()
                if not records:
                    return "No license data found. Run 'pf-agent refresh' first."
                
                summary = []
                for record in records:
                    summary.append(f"{record['instance_id']}: {record['status']} (expires {record['expiry_date'][:10]})")
                
                return "License Summary:\n" + "\n".join(summary)
        except Exception as e:
            return f"Error: {e}"
    
    # Classify intent
    intent, confidence = classifier.classify(query)
    
    # Extract instance hint from query if not provided
    if not instance_hint:
        instance_hint = classifier.extract_instance_hint(query)
    
    # Create appropriate task based on intent
    if intent == Intent.APPLY_LICENSE:
        agent = create_license_updater()
        task = Task(
            description=f"Help user apply a license update. Query: '{query}'. Instance hint: {instance_hint or 'none'}",
            expected_output="Clear guidance on license application process in plain text format",
            agent=agent
        )
    else:
        # Default to get license details
        agent = create_license_getter()
        task = Task(
            description=f"Retrieve license information. Query: '{query}'. Instance hint: {instance_hint or 'none'}",
            expected_output="License status information in clear, human-readable plain text format. Use numbered lists or simple text, not JSON.",
            agent=agent
        )
    
    # Execute task with crew
    crew = Crew(
        agents=[agent],
        tasks=[task],
        verbose=False
    )
    
    try:
        result = crew.kickoff()
        return str(result)
    except Exception as e:
        # Print detailed error information for debugging
        print(f"⚠️  CrewAI Error: {type(e).__name__}: {e}")
        import traceback
        print(f"📍 Error details: {traceback.format_exc()}")
        print("💡 Falling back to direct service call...")
        
        # Fallback to direct service call if CrewAI fails
        service = LicenseService()
        
        if intent == Intent.APPLY_LICENSE:
            return f"License application requires explicit command: pf-agent license apply --instance <id> --file <path>"
        else:
            try:
                if instance_hint:
                    record = service.get_license(instance_hint)
                    return f"License for {instance_hint}: Status={record['status']}, Expires={record['expiry_date'][:10]}, Days={record['days_to_expiry']}"
                else:
                    records = service.get_all_licenses()
                    if not records:
                        return "No license data found. Run 'pf-agent refresh' first."
                    
                    summary = []
                    for record in records:
                        summary.append(f"{record['instance_id']}: {record['status']} (expires {record['expiry_date'][:10]})")
                    
                    return "License Summary:\n" + "\n".join(summary)
            except Exception as service_error:
                return f"Error: {service_error}"
