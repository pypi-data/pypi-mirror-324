from uuid import UUID
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from enum import Enum
from typing import Optional, List, Dict, Literal

from dhisana.schemas.common import User

# -----------------------------
# Lead-List-Specific Schemas
# -----------------------------

class Lead(BaseModel):
    id: Optional[str] = None
    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    user_linkedin_url: Optional[str] = None
    primary_domain_of_organization: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    headline: Optional[str] = None
    lead_location: Optional[str] = None
    organization_name: Optional[str] = None
    organization_website: Optional[str] = None
    summary_about_lead: Optional[str] = None
    workflow_stage: Optional[str] = None
    assigned_to: Optional[str] = None
    engaged: Optional[bool] = None
    last_contact: Optional[int] = None
    additional_properties: Optional[Dict[str, str]] = None
    research_summary: Optional[str] = None
    task_ids: Optional[List[str]] = None
    email_validation_status: Optional[
        Literal["not_started", "in_progress", "valid", "invalid"]
    ] = None
    linkedin_validation_status: Optional[
        Literal["not_started", "in_progress", "valid", "invalid"]
    ] = None
    research_status: Optional[
        Literal["not_started", "in_progress", "done", "failed"]
    ] = None
    enchrichment_status: Optional[
        Literal["not_started", "in_progress", "done", "failed"]
    ] = None


class LeadList(BaseModel):
    id: Optional[str] = None
    name: str
    sources: List[str]
    tags: List[str]
    category: str
    leads_count: int
    assigned_users: List[str]
    updated_at: int
    status: Literal["connected", "disconnected", "coming soon"]
    leads: Optional[List[Lead]] = None
    public: Optional[bool] = None

# -----------------------------
# Task-Specific Schemas
# -----------------------------

class TaskStatus(str, Enum):
    PENDING = "PENDING"
    RUNNING = "RUNNING"
    FAILED = "FAILED"
    COMPLETED = "COMPLETED"

class TaskBase(BaseModel):
    name: str
    task_type: str
    data_id: Optional[UUID] = None
    data_type: Optional[str] = None

    inputs: Optional[List[Dict[str, Any]]] = []
    outputs: Optional[List[Dict[str, Any]]] = []

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    status: Optional[TaskStatus] = None
    logs: Optional[List[Any]] = None
    metrics: Optional[Dict[str, Any]] = None
    outputs: Optional[List[Dict[str, Any]]] = None

class Task(TaskBase):
    id: UUID
    status: TaskStatus
    logs: List[Any] = []
    metrics: Dict[str, Any] = {}
    created_at: int                 # store as ms since epoch
    updated_at: int
    completed_at: Optional[int] = None

    class Config:
        from_attributes = True


# -----------------------------
# Campaign-Specific Schemas
# -----------------------------

class SendRules(BaseModel):
    daily_send_limit: Optional[int] = None
    concurrency_limit: Optional[int] = None
    time_window_start: Optional[str] = None  # "HH:MM" string
    time_window_end: Optional[str] = None
    block_weekends: Optional[bool] = False

class Touch(BaseModel):
    type: str            # e.g. 'email', 'linkedin', ...
    action: str          # e.g. 'view_linkedin_profile', 'send_connection_request'
    details: str
    delay_days: int
    template_id: Optional[str] = None

class PromptEngineeringGuidance(BaseModel):
    tone: str
    word_count: int
    paragraphs: int

class LeadLog(BaseModel):
    id: Optional[str] = None
    message: str
    channel: Optional[str] = None
    timestamp: int                   # ms since epoch
    status: Optional[str] = None

class CampaignLead(BaseModel):
    id: Optional[str] = None
    campaign_id: str
    lead_list_id: Optional[str] = None
    lead_id: Optional[str] = None
    lead_name: str

    status: Optional[str] = None  # 'PENDING', 'WAITING_APPROVAL', 'OUTBOUND_PENDING', 'COMPLETED'
    current_step: Optional[int] = 0
    total_steps: Optional[int] = 0
    engaged: Optional[bool] = False
    last_touch: Optional[str] = None
    created_at: Optional[int] = None      # ms since epoch
    updated_at: Optional[int] = None

    logs: Optional[List[LeadLog]] = None

class CampaignCounter(BaseModel):
    id: Optional[str] = None
    campaign_id: str
    date: str                 # "YYYY-MM-DD"
    daily_sends: int
    current_concurrency: int

class CampaignStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    PAUSED = "PAUSED"
    COMPLETED = "COMPLETED"

class PendingEvent(BaseModel):
    event_id: str
    lead_id: str
    touch_index: int
    channel: str
    action: str
    subject: str
    message: str
    created_at: int             # ms since epoch

class Campaign(BaseModel):
    id: str
    name: str
    description: str
    lead_lists: List[str]
    run_mode: str
    updated_at: int                       # ms since epoch

    tags: Optional[List[str]] = None
    channel: Optional[str] = None
    mission_objective: Optional[str] = None
    mission_progress: Optional[int] = None
    ai_alerts: Optional[List[str]] = None
    automatic_adjustments: Optional[List[str]] = None

    product_name: Optional[str] = None
    value_prop: Optional[str] = None
    call_to_action: Optional[str] = None
    pain_points: Optional[List[str]] = None
    proof_points: Optional[List[str]] = None
    prompt_engineering_guidance: Optional[PromptEngineeringGuidance] = None
    prompt_templates: Optional[List[Dict[str, Any]]] = None
    touches: Optional[List[Touch]] = None
    send_rules: Optional[SendRules] = None

    status: Optional[CampaignStatus] = None
    start_date: Optional[int] = None      # ms since epoch
    pause_date: Optional[int] = None
    end_date: Optional[int] = None

    leads: Optional[List[CampaignLead]] = None
    counter: Optional[CampaignCounter] = None
    pending_events: Optional[List[PendingEvent]] = None

    class Config:
        from_attributes = True

class ChannelType(str, Enum):
    NEW_EMAIL = "new_email"
    LINKEDIN_CONNECT_MESSAGE = "linkedin_connect_message"
    REPLY_EMAIL = "reply_email"
    LINKEDIN_USER_MESSAGE = "linkedin_user_message"
    
class ContentGenerationContext(BaseModel):
    product_name: Optional[str] = None
    value_prop: Optional[str] = None
    call_to_action: Optional[str] = None
    pain_points: Optional[List[str]] = None
    proof_points: Optional[List[str]] = None
    prompt_engineering_guidance: Optional[PromptEngineeringGuidance] = None

    lead_info: Lead
    
    sender_full_name: str
    sender_first_name: str
    sender_last_name: str

    email_subject_template: str
    email_body_template: str
    external_source_fileIds: Dict[str, Any]
    external_openai_vector_store_id: Optional[str]
    additional_instructions: str
    
    current_email_thread: str
    email_triage_guidelines: str
    
    current_linkedin_thread: str
    linkedin_triage_guidelines: str
    
    target_channel_type: ChannelType
        
# --------------------------------------------------------------------
# 1. Define your HubSpotLeadInformation model
# --------------------------------------------------------------------
class HubSpotLeadInformation(BaseModel):
    full_name: str = Field("", description="Full name of the lead")
    first_name: str = Field("", description="First name of the lead")
    last_name: str = Field("", description="Last name of the lead")
    email: str = Field("", description="Email address of the lead")
    user_linkedin_url: str = Field("", description="LinkedIn URL of the lead")
    primary_domain_of_organization: str = Field("", description="Primary domain of the organization")
    job_title: str = Field("", description="Job Title of the lead")
    phone: str = Field("", description="Phone number of the lead")
    headline: str = Field("", description="Headline of the lead")
    lead_location: str = Field("", description="Location of the lead")
    organization_name: str = Field("", description="Current Company where lead works")
    organization_website: str = Field("", description="Current Company website of the lead")
    organization_linkedin_url : str = Field("", description="Company LinkedIn URL")
    # additional_properties is dict of dict-of-strings. 
    # We store all unmapped HubSpot fields as string => string.
    additional_properties: Dict[str, Dict[str, str]] = Field(
        default_factory=lambda: {"hubspot_lead_information": {}},
        description="Store all extra HubSpot fields not mapped to standard ones"
    )

# --------------------------------------------------------------------
# 2. Map HubSpot property names -> HubSpotLeadInformation fields
# --------------------------------------------------------------------
HUBSPOT_TO_LEAD_MAPPING = {
    "firstname": "first_name",
    "lastname": "last_name",
    "email": "email",
    "phone": "phone",
    "jobtitle": "job_title",            # Default HubSpot job title property
    "company": "organization_name",     # Map "company" -> "organization_name"
    "website": "organization_website",  # Map "website" -> "organization_website"
    "address": "lead_location",         # You can choose "city", "state", etc. if you prefer
    "city": "lead_location",
    "domain": "primary_domain_of_organization",
}



class SmartListStatus(str, Enum):
    DRAFT = "DRAFT"
    ACTIVE = "ACTIVE"
    COMPLETED = "COMPLETED"


class SmartList(BaseModel):
    id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None
    instructions: Optional[str] = None
    max_leads: Optional[int] = None
    use_online_search: Optional[bool] = False
    category: Optional[str] = None

    status: SmartListStatus = SmartListStatus.DRAFT
    start_date: Optional[int] = None
    end_date: Optional[int] = None

    agent_instance_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    created_at: Optional[int] = None
    updated_by: Optional[UUID] = None
    updated_at: Optional[int] = None

    class Config:
        from_attributes = True


class SmartListLead(BaseModel):
    id: Optional[UUID] = None

    smart_list_id: Optional[UUID] = None

    full_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[str] = None
    user_linkedin_url: Optional[str] = None
    user_linkedin_salesnav_url: Optional[str] = None
    organization_linkedin_url: Optional[str] = None
    organization_linkedin_salesnav_url: Optional[str] = None
    primary_domain_of_organization: Optional[str] = None
    job_title: Optional[str] = None
    phone: Optional[str] = None
    headline: Optional[str] = None
    lead_location: Optional[str] = None
    organization_name: Optional[str] = None
    organization_website: Optional[str] = None
    summary_about_lead: Optional[str] = None
    keywords: Optional[List[str]] = None
    additional_properties: Optional[Dict[str, str]] = None
    research_summary: Optional[str] = None

    qualification_score: Optional[float] = None
    qualification_reason: Optional[str] = None
    source: Optional[str] = None

    agent_instance_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    created_at: Optional[int] = None
    updated_by: Optional[UUID] = None
    updated_at: Optional[int] = None

    class Config:
        from_attributes = True


class SmartListLog(BaseModel):
    id: Optional[UUID] = None
    message: str

    smart_list_id: UUID

    agent_instance_id: Optional[UUID] = None
    organization_id: Optional[UUID] = None
    created_by: Optional[UUID] = None
    created_at: Optional[int] = None
    updated_by: Optional[UUID] = None
    updated_at: Optional[int] = None

    class Config:
        from_attributes = True

class LeadsQueryFilters(BaseModel):
    """
    Defines the filter parameters used to query leads in the Apollo database.
    All fields are optional and will default to None if not specified by user.
    """
    # Existing fields
    job_titles_to_search: Optional[List[str]] = Field(
        default=None, 
        description="List of job titles to include in the search."
    )
    locations_to_search: Optional[List[str]] = Field(
        default=None, 
        description="List of personal locations (cities, states, countries)."
    )
    min_number_of_employees_in_organization: Optional[int] = Field(
        default=None, 
        description="Minimum number of employees (>=1). Default=1 if omitted."
    )
    max_number_of_employees_in_organization: Optional[int] = Field(
        default=None, 
        description="Maximum number of employees (<=100000). Default=1000 if omitted."
    )
    filter_by_signals: Optional[List[str]] = Field(
        default=None, 
        description="List of signals to filter by, e.g. ['RECENT_JOB_CHANGE']."
    )
    max_number_of_items_to_return: Optional[int] = Field(
        default=None, 
        description="Max # of items (<=5000). Default=100."
    )
    industries: Optional[List[str]] = Field(
        default=None, 
        description="List of industries. Default=[] if omitted."
    )

    # Fields that were not previously used by the search, but can exist
    min_revenue_of_the_company: Optional[int] = Field(
        default=None, 
        description="Minimum company revenue (not currently used in People Search)."
    )
    max_revenue_of_the_company: Optional[int] = Field(
        default=None, 
        description="Maximum company revenue (not currently used in People Search)."
    )
    job_functions: Optional[List[str]] = Field(
        default=None, 
        description="List of job functions (not directly used by the new People Search)."
    )

    # --------------------------------------------------
    # New fields from the updated Apollo doc
    # --------------------------------------------------
    q_keywords: Optional[str] = Field(
        default=None,
        description="A string of keywords to filter results."
    )
    organization_domains: Optional[List[str]] = Field(
        default=None,
        description="Domains of the person's employer (e.g., ['microsoft.com'])."
    )
    organization_locations: Optional[List[str]] = Field(
        default=None,
        description="List of HQ locations for the employer (city, state, country)."
    )
    contact_email_status: Optional[List[str]] = Field(
        default=None,
        description="Email statuses to filter by, e.g. ['verified', 'unavailable']."
    )
    organization_ids: Optional[List[str]] = Field(
        default=None,
        description="Apollo IDs for the companies/employers (string IDs)."
    )
    person_seniorities: Optional[List[str]] = Field(
        default=None,
        description="List of job seniorities, e.g. ['manager', 'director', 'vp']. "
                    "Apollo supports: owner, founder, c_suite, partner, vp, head, "
                    "director, manager, senior, entry, intern."
    )

