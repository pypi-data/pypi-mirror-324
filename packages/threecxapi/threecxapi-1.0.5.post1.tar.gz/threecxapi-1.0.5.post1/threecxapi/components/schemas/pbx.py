from decimal import Decimal
from enum import auto
from uuid import UUID
from datetime import datetime
from typing import Optional
from pydantic import Field
from threecxapi.components.schema import Schema
from threecxapi.components.schemas.enums import (
    AddedBy,
    AnimationStyle,
    Authentication,
    AuthenticationType,
    BlockType,
    ButtonIconType,
    CallHandlingFlags,
    ChatRecipientsType,
    ChatType,
    ContactType,
    DayOfWeek,
    DestinationType,
    DeviceType,
    DirectionType,
    DnType,
    EditorType,
    EventLogType,
    FailoverCondition,
    FailoverMode,
    FileSystemType,
    GatewayType,
    GroupHoursMode,
    IntegrationSyncType,
    IPInRegistrationContactType,
    IVRForwardType,
    IVRType,
    LiveChatCommunication,
    LiveChatGreeting,
    LiveChatLanguage,
    LiveChatMessageDateformat,
    LiveChatMinimizedStyle,
    LiveMessageUserinfoFormat,
    MailServerType,
    MatchingStrategyType,
    OfficeHoursBits,
    ParameterType,
    PeerType,
    PhonebookPriorityOptions,
    PhoneDeviceVlanType,
    PmsIntegrationType,
    PollingStrategyType,
    ProfileType,
    PromptSetType,
    PromptType,
    ProvType,
    QueueNotifyCode,
    QueueRecording,
    RecordingCallType,
    ReferenceNumeric,
    RequireRegistrationForType,
    ResetQueueStatisticsFrequency,
    RuleCallTypeType,
    RuleConditionType,
    RuleHoursType,
    ScheduleType,
    ServiceStatus,
    SplitDNSConversionState,
    SRTPModeType,
    StartupLicense,
    StrategyType,
    TemplateType,
    TranscriptionLevel,
    TrunkEditorType,
    TrunkVariableType,
    TypeOfAutoPickupForward,
    TypeOfCDRLog,
    TypeOfChatOwnershipType,
    TypeOfIPDestriction,
    TypeOfPhoneBookAddQueueName,
    TypeOfPhoneBookDisplay,
    TypeOfPhoneBookResolving,
    TypeOfTransportRestriction,
    TypeOfUser,
    UpdateType,
    UserTag,
    VMEmailOptionsType,
    VMPlayMsgDateTimeType,
    XferTypeEnum,
    XOperatingSystemType,
)
from threecxapi.util import TcxStrEnum


class OauthStateParam(Schema):
    RedirectUri: str
    Variable: str


class OauthState(Schema):
    State: Optional[str] = None


class CrmTemplateSource(Schema):
    Value: Optional[str] = None


class Rights(Schema):
    AllowIVR: Optional[bool] = None
    AllowParking: Optional[bool] = None
    AllowToChangePresence: Optional[bool] = None
    AllowToManageCompanyBook: Optional[bool] = None
    AssignClearOperations: Optional[bool] = None
    CanBargeIn: Optional[bool] = None
    CanIntercom: Optional[bool] = None
    CanSeeGroupCalls: Optional[bool] = None
    CanSeeGroupMembers: Optional[bool] = None
    CanSeeGroupRecordings: Optional[bool] = None
    PerformOperations: Optional[bool] = None
    RoleName: str
    ShowMyCalls: Optional[bool] = None
    ShowMyPresence: Optional[bool] = None
    ShowMyPresenceOutside: Optional[bool] = None


class ResetQueueStatisticsSchedule(Schema):
    Day: Optional[DayOfWeek] = None
    Frequency: Optional[ResetQueueStatisticsFrequency] = None
    Time: Optional[str] = None


class PhoneLldpInfo(Schema):
    Configurable: Optional[bool] = None
    Value: Optional[bool] = None


class PhoneDeviceVlanInfo(Schema):
    Configurable: Optional[bool] = None
    Enabled: Optional[bool] = None
    Priority: Optional[int] = None
    PriorityConfigurable: Optional[bool] = None
    PriorityMax: Optional[int] = None
    PriorityMin: Optional[int] = None
    Type: Optional[PhoneDeviceVlanType] = None
    VlanId: Optional[int] = None
    VlanIdMax: Optional[int] = None
    VlanIdMin: Optional[int] = None


class CustomQueueRingtone(Schema):
    Queue: Optional[str] = None
    Ringtone: Optional[str] = None


class PhoneModel(Schema):
    AddAllowed: Optional[bool] = None
    CanBeSBC: Optional[bool] = None
    Name: Optional[str] = None
    URL: Optional[str] = None
    UserAgent: Optional[str] = None


class TrunkVariable(Schema):
    DefaultValue: Optional[str] = None
    MaxLength: Optional[int] = None
    MinLength: Optional[int] = None
    Name: Optional[str] = None
    Option: Optional[str] = None
    OptionType: Optional[TrunkVariableType] = None
    Pattern: Optional[str] = None
    Prompt: Optional[str] = None
    Required: Optional[bool] = None
    Title: Optional[str] = None
    Validation: Optional[str] = None


class BackupSchedule(Schema):
    Day: Optional[DayOfWeek] = None
    RepeatHours: Optional[int] = None
    schedule_type: Optional[ScheduleType] = Field(None, alias="ScheduleType")
    Time: Optional[str] = None


class LocationSettings(Schema):
    file_system_type: Optional[FileSystemType] = Field(None, alias="FileSystemType")
    FtpPassword: Optional[str] = None
    FtpPath: Optional[str] = None
    FtpUser: Optional[str] = None
    GbJson: Optional[str] = None
    GbJsonFileName: Optional[str] = None
    GbPath: Optional[str] = None
    LocalPath: Optional[str] = None
    NsDomain: Optional[str] = None
    NsPassword: Optional[str] = None
    NsPath: Optional[str] = None
    NsUser: Optional[str] = None
    SftpPassword: Optional[str] = None
    SftpPath: Optional[str] = None
    SftpPrivateKey: Optional[str] = None
    SftpPrivateKeyName: Optional[str] = None
    SftpUser: Optional[str] = None
    SharePointPath: Optional[str] = None


class GroupProps(Schema):
    DectMaxCount: Optional[int] = None
    Fqdn: Optional[str] = None
    LiveChatMaxCount: Optional[int] = None
    PersonalContactsMaxCount: Optional[int] = None
    PromptsMaxCount: Optional[int] = None
    ResellerId: Optional[str] = None
    ResellerName: Optional[str] = None
    SbcMaxCount: Optional[int] = None
    startup_license: Optional[StartupLicense] = Field(None, alias="StartupLicense")
    StartupOwnerEmail: Optional[str] = None
    SubcriptionExpireDate: Optional[datetime]
    Subscription: Optional[str] = None
    SubscriptionType: Optional[str] = None
    SystemNumberFrom: Optional[str] = None
    SystemNumberTo: Optional[str] = None
    TrunkNumberFrom: Optional[str] = None
    TrunkNumberTo: Optional[str] = None
    UserNumberFrom: Optional[str] = None
    UserNumberTo: Optional[str] = None


class Holiday(Schema):
    Day: Optional[int] = None
    DayEnd: Optional[int] = None
    HolidayPrompt: Optional[str] = None
    Id: int
    IsRecurrent: Optional[bool] = None
    Month: Optional[int] = None
    MonthEnd: Optional[int] = None
    Name: Optional[str] = None
    TimeOfEndDate: Optional[str] = None
    TimeOfStartDate: Optional[str] = None
    Year: Optional[int] = None
    YearEnd: Optional[int] = None


class EntityRestrictions(Schema):
    Allowed: Optional[int] = None
    Unlimited: Optional[bool] = None
    Used: Optional[int] = None


class OutboundRoute(Schema):
    Append: Optional[str] = None
    CallerID: Optional[str] = None
    Prepend: Optional[str] = None
    StripDigits: Optional[int] = None
    TrunkId: Optional[int] = None
    TrunkName: Optional[str] = None


class DNRange(Schema):
    From: Optional[str] = None
    To: Optional[str] = None


class PeerGroup(Schema):
    GroupID: int
    Name: Optional[str] = None
    Number: Optional[str] = None
    RoleName: Optional[str] = None


class TrunkMessaging(Schema):
    Enabled: Optional[bool] = None
    Provider: Optional[str] = None
    Webhook: Optional[str] = None
    # The schema specifies an additional property for this object is type string.
    # I'm not entirley sure what it means by this.
    # additionalProperties: str


class GatewayParameterBinding(Schema):
    Custom: Optional[str] = None
    ParamId: int
    ValueId: int


class Choice(Schema):
    Key: str
    Value: str


class CIDFormatting(Schema):
    Priority: Optional[int] = None
    ReplacePattern: Optional[str] = None
    SourcePattern: Optional[str] = None


class SetRoute(Schema):
    DID: str
    DisplayName: Optional[str] = None
    TrunkId: int


class KeyValuePair_2OfString_String(Schema):
    pass


class FxsProvisioning(Schema):
    LocalAudioPortEnd: Optional[int] = None
    LocalAudioPortStart: Optional[int] = None
    LocalInterface: Optional[str] = None
    LocalSipPort: Optional[int] = None
    Method: Optional[ProvType] = None
    ProvLink: Optional[str] = None
    RemoteFQDN: Optional[str] = None
    RemotePort: Optional[int] = None
    SbcName: Optional[str] = None


class DeviceLine(Schema):
    Key: int
    Name: Optional[str] = None
    Number: str


class Variable(Schema):
    Name: str
    Value: str


class FxsModel(Schema):
    DisplayName: str
    UserAgent: str


class FxsVariableChoice(Schema):
    DisplayName: str
    Name: str


class FxsVariable(Schema):
    Choices: Optional[list[FxsVariableChoice]] = Field(default=None)
    Name: str
    Title: str
    ValidationType: Optional[str] = None


class Prompt(Schema):
    Filename: Optional[str] = None
    Id: str
    Transcription: Optional[str] = None


class WebsiteLinksTranslations(Schema):
    AuthenticationMessage: Optional[str] = None
    EndingMessage: Optional[str] = None
    FirstResponseMessage: Optional[str] = None
    GdprMessage: Optional[str] = None
    GreetingMessage: Optional[str] = None
    GreetingOfflineMessage: Optional[str] = None
    InviteMessage: Optional[str] = None
    OfflineEmailMessage: Optional[str] = None
    OfflineFinishMessage: Optional[str] = None
    OfflineFormInvalidEmail: Optional[str] = None
    OfflineFormInvalidName: Optional[str] = None
    OfflineFormMaximumCharactersReached: Optional[str] = None
    OfflineNameMessage: Optional[str] = None
    StartChatButtonText: Optional[str] = None
    UnavailableMessage: Optional[str] = None
    WindowTitle: Optional[str] = None


class LiveChatStyling(Schema):
    Animation: Optional[AnimationStyle] = None
    Minimized: Optional[bool] = None
    Style: Optional[str] = None
    UseRubik: Optional[bool] = None


class GeneralLiveChatSettings(Schema):
    AllowSoundNotifications: Optional[bool] = None
    authentication: Optional[Authentication] = Field(None, alias="Authentication")
    DisableOfflineMessages: Optional[bool] = None
    EnableGA: Optional[bool] = None
    EnableOnMobile: Optional[bool] = None
    GdprEnabled: Optional[bool] = None
    Greeting: Optional[LiveChatGreeting] = None


class LiveChatAdvancedSettings(Schema):
    CallTitle: Optional[str] = None
    CommunicationOptions: Optional[LiveChatCommunication] = None
    EnableDirectCall: Optional[bool] = None
    IgnoreQueueOwnership: Optional[bool] = None


class LiveChatBox(Schema):
    button_icon_type: Optional[ButtonIconType] = Field(None, alias="ButtonIconType")
    ButtonIconUrl: Optional[str] = None
    ChatDelay: Optional[int] = None
    Height: Optional[str] = None
    live_chat_language: Optional[LiveChatLanguage] = Field(None, alias="LiveChatLanguage")
    live_message_userinfo_format: Optional[LiveMessageUserinfoFormat] = Field(None, alias="LiveMessageUserinfoFormat")
    MessageDateformat: Optional[LiveChatMessageDateformat] = None
    MinimizedStyle: Optional[LiveChatMinimizedStyle] = None
    OperatorIcon: Optional[str] = None
    OperatorName: Optional[str] = None
    ShowOperatorActualName: Optional[bool] = None
    WindowIcon: Optional[str] = None


class UpdateItem(Schema):
    Category: str
    Description: str
    DescriptionLink: str
    Guid: UUID = None
    Ignore: Optional[bool] = None
    Image: str
    LocalVersion: str
    Name: str
    OutOfDate: Optional[bool] = None
    ServerVersion: str
    update_type: Optional[UpdateType] = Field(None, alias="UpdateType")


class CategoryUpdate(Schema):
    Category: Optional[str] = None
    Count: int


class BackupContents(Schema):
    CallHistory: Optional[bool] = None
    EncryptBackup: Optional[bool] = None
    EncryptBackupPassword: Optional[str] = None
    FQDN: Optional[bool] = None
    License: Optional[bool] = None
    PhoneProvisioning: Optional[bool] = None
    Prompts: Optional[bool] = None
    Recordings: Optional[bool] = None
    VoiceMails: Optional[bool] = None


class QualityParty(Schema):
    AddressStr: Optional[str] = None
    Burst: Optional[int] = None
    Codec: Optional[str] = None
    Duration: Optional[int] = None
    Inbound: Optional[bool] = None
    MOSFromPBX: Optional[float | ReferenceNumeric] = None
    MOSToPBX: Optional[float | ReferenceNumeric] = None
    Number: Optional[str] = None
    RTT: Optional[float | ReferenceNumeric] = None
    RxJitter: Optional[float | ReferenceNumeric] = None
    RxLost: Optional[float | ReferenceNumeric] = None
    RxPackets: Optional[int] = None
    TunAddressStr: Optional[str] = None
    TxBursts: Optional[int] = None
    TxJitter: Optional[float | ReferenceNumeric] = None
    TxLost: Optional[float | ReferenceNumeric] = None
    TxPackets: Optional[int] = None
    UserAgent: Optional[str] = None


class CrmParameter(Schema):
    Default: Optional[str] = None
    Editor: Optional[EditorType] = None
    ListValues: Optional[list[str]] = None
    ListValuesText: Optional[str] = None
    Name: Optional[str] = None
    Parent: Optional[str] = None
    RequestUrl: Optional[str] = None
    RequestUrlParameters: Optional[str] = None
    ResponseScenario: Optional[str] = None
    Title: Optional[str] = None
    Type: Optional[ParameterType] = None
    Validation: Optional[str] = None


class CrmAuthentication(Schema):
    Type: Optional[AuthenticationType] = None
    Values: Optional[list[str]] = None


class CDRSettingsField(Schema):
    Length: Optional[int] = None
    Name: Optional[str] = None


class ADUsersSyncConfiguration(Schema):
    EnableSSO: Optional[bool] = None
    IsEnabled: Optional[bool] = None
    IsSyncOfficePhone: Optional[bool] = None
    IsSyncPhoto: Optional[bool] = None
    SelectedUsers: Optional[list[str]] = None
    StartingExtensionNumber: str
    SyncEvents: Optional[bool] = None
    SyncGuestUsers: Optional[bool] = None
    SyncPersonalContacts: Optional[bool] = None
    SyncType: Optional[IntegrationSyncType] = None


class UsersSyncConfiguration(Schema):
    IsEnabled: Optional[bool] = None
    SelectedUsers: Optional[list[str]] = None
    SyncType: Optional[IntegrationSyncType] = None


class License(Schema):
    IsMaintainceExpired: Optional[bool] = None
    ProductCode: Optional[str] = None


class CrmContact(Schema):
    CompanyName: Optional[str] = None
    ContactRawData: Optional[str] = None
    contact_type: Optional[ContactType] = Field(None, alias="ContactType")
    ContactUrl: Optional[str] = None
    Department: Optional[str] = None
    Email: Optional[str] = None
    FaxBusiness: Optional[str] = None
    FirstName: Optional[str] = None
    LastName: Optional[str] = None
    Pager: Optional[str] = None
    PhoneBusiness: Optional[str] = None
    PhoneBusiness2: Optional[str] = None
    PhoneHome: Optional[str] = None
    PhoneMobile: Optional[str] = None
    PhoneMobile2: Optional[str] = None
    PhoneOther: Optional[str] = None
    PhotoUrl: Optional[str] = None
    Title: Optional[str] = None


class Destination(Schema):
    External: Optional[str] = None
    Name: Optional[str] = None
    Number: Optional[str] = None
    peer_type: Optional[PeerType] = Field(None, alias="PeerType")
    To: Optional[DestinationType] = None


class Route(Schema):
    IsPromptEnabled: Optional[bool] = None
    Prompt: Optional[str] = None
    Route: Optional[Destination] = None


class FirstAvailableNumber(Schema):
    Number: Optional[str] = None


class BlackListNumber(Schema):
    CallerId: str
    Description: Optional[str] = None
    Id: str


class BlocklistAddr(Schema):
    added_by: Optional[AddedBy] = Field(None, alias="AddedBy")
    block_type: Optional[BlockType] = Field(None, alias="BlockType")
    Description: Optional[str] = None
    ExpiresAt: Optional[datetime]
    Id: int
    IPAddrMask: Optional[str] = None


class ReceptionistForward(Schema):
    CustomData: Optional[str] = None
    ForwardDN: Optional[str] = None
    ForwardType: IVRForwardType
    Id: int
    Input: Optional[str] = None
    peer_type: Optional[PeerType] = Field(None, alias="PeerType")


class UserGroup(Schema):
    CanDelete: Optional[bool] = None
    GroupId: Optional[int] = None
    Id: Optional[int] = None
    MemberName: Optional[str] = None
    Name: Optional[str] = None
    Number: Optional[str] = None
    rights: Optional[Rights] = Field(None, alias="Rights")
    Type: Optional[DnType] = None


class Receptionist(Schema):
    BreakRoute: Optional[Route] = None
    Forwards: list[ReceptionistForward] = Field(default_factory=list)
    ForwardSmsTo: Optional[str] = None
    Groups: list[UserGroup] = Field(default_factory=list)
    HolidaysRoute: Optional[Route] = None
    Id: int
    InvalidKeyForwardDN: Optional[str] = None
    IsRegistered: Optional[bool] = None
    ivr_type: Optional[IVRType] = Field(None, alias="IVRType")
    Name: Optional[str] = None
    Number: Optional[str] = None
    OfficeRoute: Optional[Route] = None
    OutOfOfficeRoute: Optional[Route] = None
    PromptFilename: Optional[str] = None
    PromptSet: Optional[str] = None
    Timeout: Optional[int] = None
    TimeoutForwardDN: Optional[str] = None
    TimeoutForwardPeerType: Optional[PeerType] = None
    TimeoutForwardType: Optional[IVRForwardType] = None
    UseMSExchange: Optional[bool] = None


class RingGroupMember(Schema):
    Id: int
    Name: Optional[str] = None
    Number: Optional[str] = None


class RingGroup(Schema):
    BreakRoute: Optional[Route] = None
    CallUsEnableChat: Optional[bool] = None
    CallUsEnablePhone: Optional[bool] = None
    CallUsEnableVideo: Optional[bool] = None
    CallUsRequirement: Optional[Authentication] = None
    ClickToCallId: Optional[str] = None
    ForwardNoAnswer: Optional[Destination] = None
    Groups: list[UserGroup] = Field(default_factory=list)
    HolidaysRoute: Optional[Route] = None
    Id: int
    IsRegistered: Optional[bool] = None
    Members: list[RingGroupMember] = Field(default_factory=list)
    MulticastAddress: Optional[str] = None
    MulticastCodec: Optional[str] = None
    MulticastPacketTime: Optional[int] = None
    MulticastPort: Optional[int] = None
    Name: Optional[str] = None
    Number: Optional[str] = None
    OfficeRoute: Optional[Route] = None
    OutOfOfficeRoute: Optional[Route] = None
    RingStrategy: Optional[StrategyType] = None
    RingTime: Optional[int] = None


class Contact(Schema):
    Business: Optional[str] = None
    Business2: Optional[str] = None
    BusinessFax: Optional[str] = None
    CompanyName: Optional[str] = None
    ContactType: Optional[str] = None
    Department: Optional[str] = None
    Email: Optional[str] = None
    FirstName: Optional[str] = None
    Home: Optional[str] = None
    Id: int
    LastName: Optional[str] = None
    Mobile2: Optional[str] = None
    Other: Optional[str] = None
    Pager: Optional[str] = None
    PhoneNumber: Optional[str] = None
    Tag: Optional[str] = None
    Title: Optional[str] = None


class IActionResult(Schema):
    pass


class QueueAgent(Schema):
    Id: Optional[int] = None
    Name: Optional[str] = None
    Number: str
    SkillGroup: Optional[str] = None


class ContactsDirSearchSettings(Schema):
    ExchangeCalendarProfileSwitching: Optional[bool] = None
    ExchangeEmailAddresses: Optional[list[str]] = None
    ExchangeFolders: Optional[list[str]] = None
    ExchangePassword: Optional[str] = None
    ExchangeServerUrl: Optional[str] = None
    ExchangeUser: Optional[str] = None


class QueueManager(Schema):
    Id: Optional[int] = None
    Name: Optional[str] = None
    Number: str


class Queue(Schema):
    AgentAvailabilityMode: Optional[bool] = None
    Agents: list[QueueAgent] = Field(default_factory=list)
    AnnouncementInterval: Optional[int] = None
    AnnounceQueuePosition: Optional[bool] = None
    BreakRoute: Optional[Route] = None
    CallbackEnableTime: Optional[int] = None
    CallbackPrefix: Optional[str] = None
    CallUsEnableChat: Optional[bool] = None
    CallUsEnablePhone: Optional[bool] = None
    CallUsEnableVideo: Optional[bool] = None
    CallUsRequirement: Optional[Authentication] = None
    ClickToCallId: Optional[str] = None
    EnableIntro: Optional[bool] = None
    ForwardNoAnswer: Optional[Destination] = None
    Groups: list[UserGroup] = Field(default_factory=list)
    HolidaysRoute: Optional[Route] = None
    Id: int
    IntroFile: Optional[str] = None
    IsRegistered: Optional[bool] = None
    Managers: list[QueueManager] = Field(default_factory=list)
    MasterTimeout: Optional[int] = None
    MaxCallersInQueue: Optional[int] = None
    Name: Optional[str] = None
    NotifyCodes: list[QueueNotifyCode] = Field(default_factory=list)
    Number: Optional[str] = None
    OfficeRoute: Optional[Route] = None
    OnHoldFile: Optional[str] = None
    OutOfOfficeRoute: Optional[Route] = None
    PlayFullPrompt: Optional[bool] = None
    PollingStrategy: Optional[PollingStrategyType] = None
    PriorityQueue: Optional[bool] = None
    PromptSet: Optional[str] = None
    Recording: Optional[QueueRecording] = None
    reset_queue_statistics_schedule: Optional[ResetQueueStatisticsSchedule] = Field(
        None, alias="ResetQueueStatisticsSchedule"
    )
    ResetStatisticsScheduleEnabled: Optional[bool] = None
    RingTimeout: Optional[int] = None
    SLATime: Optional[int] = None
    type_of_chat_ownership_type: Optional[TypeOfChatOwnershipType] = Field(None, alias="TypeOfChatOwnershipType")
    WrapUpTime: Optional[int] = None


class Period(Schema):
    day_of_week: Optional[DayOfWeek] = Field(None, alias="DayOfWeek")
    Start: Optional[str] = None
    Stop: Optional[str] = None


class Schedule(Schema):
    IgnoreHolidays: Optional[bool] = None
    Periods: Optional[list[Period]] = None
    Type: RuleHoursType


class ExtensionRule(Schema):
    CallerId: Optional[str] = None
    destination: Optional[Destination] = Field(None, alias="Destination")
    Hours: Optional[Schedule] = None
    Id: int


class AvailableRouting(Schema):
    BusyAllCalls: Optional[bool] = None
    BusyExternal: Optional[Destination] = None
    BusyInternal: Optional[Destination] = None
    NoAnswerAllCalls: Optional[bool] = None
    NoAnswerExternal: Optional[Destination] = None
    NoAnswerInternal: Optional[Destination] = None
    NotRegisteredAllCalls: Optional[bool] = None
    NotRegisteredExternal: Optional[Destination] = None
    NotRegisteredInternal: Optional[Destination] = None


class AwayRouting(Schema):
    AllHoursExternal: Optional[bool] = None
    AllHoursInternal: Optional[bool] = None
    External: Optional[Destination] = None
    Internal: Optional[Destination] = None


class ForwardingProfile(Schema):
    AcceptMultipleCalls: Optional[bool] = None
    AvailableRoute: Optional[AvailableRouting] = None
    AwayRoute: Optional[AwayRouting] = None
    BlockPushCalls: Optional[bool] = None
    CustomMessage: Optional[str] = None
    CustomName: Optional[str] = None
    DisableRingGroupCalls: Optional[bool] = None
    # Id: int
    Name: Optional[str] = None
    NoAnswerTimeout: Optional[int] = None
    OfficeHoursAutoQueueLogOut: Optional[bool] = None
    RingMyMobile: Optional[bool] = None


class Greeting(Schema):
    DisplayName: Optional[str] = None
    Filename: Optional[str] = None
    Type: ProfileType


class TwoFactorAuth(Schema):
    ManualEntryKey: Optional[str] = None
    ProvisionUrl: Optional[str] = None


class MonitoringState(Schema):
    DN: str
    Expiration: int


class PhoneRegistrar(Schema):
    Capabilities: Optional[int] = None
    FirmwareAvailable: Optional[str] = None
    FirmwareVersion: Optional[str] = None
    InterfaceLink: Optional[str] = None
    IpAddress: Optional[str] = None
    MAC: Optional[str] = None
    Model: Optional[str] = None
    PhoneWebPassword: Optional[str] = None
    ProvLink: Optional[str] = None
    UserAgent: Optional[str] = None
    Vendor: Optional[str] = None


class PhoneTemplate(Schema):
    AddAllowed: Optional[bool] = None
    AllowedNetConfigs: Optional[list[str]] = None
    AllowSSLProvisioning: Optional[bool] = None
    BacklightTimeouts: Optional[list[str]] = None
    Codecs: Optional[list[str]] = None
    Content: Optional[str] = None
    DateFormats: Optional[list[str]] = None
    DefaultQueueRingTone: Optional[str] = None
    HotdeskingAllowed: Optional[bool] = None
    Id: str
    IsCustom: Optional[bool] = None
    Languages: Optional[list[str]] = None
    MaxQueueCustomRingtones: Optional[int] = None
    Models: Optional[list[PhoneModel]] = None
    PowerLedSettings: Optional[list[str]] = None
    QueueRingTones: Optional[list[str]] = None
    RingTones: Optional[list[str]] = None
    RpsEnabled: Optional[bool] = None
    ScreenSaverTimeouts: Optional[list[str]] = None
    template_type: Optional[TemplateType] = Field(None, alias="TemplateType")
    TimeFormats: Optional[list[str]] = None
    TimeZones: Optional[list[str]] = None
    URL: Optional[str] = None
    XferTypeEnabled: Optional[bool] = None


class TrunkMessagingTemplate(Schema):
    MessagingVariables: Optional[list[TrunkVariable]] = None
    _Optional: Optional[bool] = None
    Outbound: Optional[bool] = None
    Provider: Optional[str] = None
    Type: Optional[str] = None


class TrunkTemplate(Schema):
    AddAllowed: Optional[bool] = None
    Content: Optional[str] = None
    Countries: Optional[list[str]] = None
    Description: Optional[str] = None
    Editors: list[TrunkEditorType] = Field(default_factory=list)
    Id: str
    MessagingTemplate: Optional[TrunkMessagingTemplate] = None
    Name: str
    Tags: Optional[list[str]] = None
    TemplateType: TemplateType
    Url: Optional[str] = None


class Recording(Schema):
    ArchivedUrl: Optional[str] = None
    CallType: Optional[RecordingCallType] = None
    EndTime: Optional[datetime]
    FromCallerNumber: Optional[str] = None
    FromCrmContact: Optional[str] = None
    FromDidNumber: Optional[str] = None
    FromDisplayName: Optional[str] = None
    FromDn: Optional[str] = None
    FromDnType: Optional[int] = None
    FromIdParticipant: Optional[int] = None
    Id: int
    IsArchived: Optional[bool] = None
    RecordingUrl: Optional[str] = None
    RefParticipantId: Optional[int] = None
    StartTime: Optional[datetime]
    ToCallerNumber: Optional[str] = None
    ToCrmContact: Optional[str] = None
    ToDidNumber: Optional[str] = None
    ToDisplayName: Optional[str] = None
    ToDn: Optional[str] = None
    ToDnType: Optional[int] = None
    ToIdParticipant: Optional[int] = None
    Transcription: Optional[str] = None


class RecordingRepositorySettings(Schema):
    AutoDeleteRecordingDays: Optional[int] = None
    AutoDeleteRecordingEnabled: Optional[bool] = None
    IsRecordingArchiveEnabled: Optional[bool] = None
    Location: Optional[LocationSettings] = None
    RecordingArchiveSchedule: Optional[BackupSchedule] = None
    RecordingDiskSpace: Optional[int] = None
    RecordingPath: Optional[str] = None
    RecordingsQuota: Optional[int] = None
    RecordingUsedSpace: Optional[int] = None


class RecordingSettings(Schema):
    CallRecordingCompression: Optional[bool] = None
    EmailWhenQuotaReachedEnabled: Optional[bool] = None
    EmailWhenQuotaReachedPercent: Optional[int] = None
    IsScheduleForArchiveEnabled: Optional[bool] = None


class SystemDirectory(Schema):
    Dirs: Optional[list[str]] = None
    Path: Optional[str] = None


class DirectoryParameters(Schema):
    Filesystem: FileSystemType
    Json: Optional[str] = None
    Path: Optional[str] = None


class Group(Schema):
    AllowCallService: Optional[bool] = None
    AnswerAfter: Optional[int] = None
    BreakRoute: Optional[Route] = None
    BreakTime: Optional[Schedule] = None
    CallHandlingMode: list[CallHandlingFlags] = Field(default_factory=list)
    CallUsEnableChat: Optional[bool] = None
    CallUsEnablePhone: Optional[bool] = None
    CallUsEnableVideo: Optional[bool] = None
    CallUsRequirement: Optional[Authentication] = None
    ClickToCallId: Optional[str] = None
    CurrentGroupHours: Optional[GroupHoursMode] = None
    CustomOperator: Optional[Destination] = None
    CustomPrompt: Optional[str] = None
    DisableCustomPrompt: Optional[bool] = None
    GloballyVisible: Optional[bool] = None
    Groups: list[UserGroup] = Field(default_factory=list)
    HasMembers: Optional[bool] = None
    HolidaysRoute: Optional[Route] = None
    Hours: Optional[Schedule] = None
    Id: int
    IsDefault: Optional[bool] = None
    Language: Optional[str] = None
    LastLoginTime: Optional[datetime] = None
    Members: list[UserGroup] = Field(default_factory=list)
    Name: Optional[str] = None
    Number: Optional[str] = None
    OfficeHolidays: list[Holiday] = Field(default_factory=list)
    OfficeRoute: Optional[Route] = None
    OutOfOfficeRoute: Optional[Route] = None
    OverrideExpiresAt: Optional[datetime] = None
    OverrideHolidays: Optional[bool] = None
    PromptSet: Optional[str] = None
    Props: Optional[GroupProps] = None
    rights: list[Rights] = Field(default_factory=list, alias="Rights")
    TimeZoneId: Optional[str] = None


class Restrictions(Schema):
    Dects: Optional[EntityRestrictions] = None
    LiveChats: Optional[EntityRestrictions] = None
    MaxPrompts: Optional[int] = None
    Sbcs: Optional[EntityRestrictions] = None
    System: Optional[EntityRestrictions] = None
    Trunks: Optional[EntityRestrictions] = None
    Users: Optional[EntityRestrictions] = None


class OutboundRule(Schema):
    DNRanges: Optional[list[DNRange]] = None
    EmergencyRule: Optional[bool] = None
    GroupIds: list[int]
    GroupNames: Optional[list[str]] = None
    Id: int
    Name: Optional[str] = None
    NumberLengthRanges: Optional[str] = None
    Prefix: Optional[str] = None
    Priority: Optional[int] = None
    Routes: Optional[list[OutboundRoute]] = None


class XOutboundRulePurge(Schema):
    Ids: list[int]


class Parameter(Schema):
    Description: Optional[str] = None
    Id: int
    Name: Optional[str] = None
    Value: Optional[str] = None


class DNProperty(Schema):
    Description: Optional[str] = None
    Id: Optional[int] = None
    Name: str
    Value: str


class Peer(Schema):
    Hidden: Optional[bool] = None
    Id: int
    MemberOf: list[PeerGroup]
    Name: Optional[str] = None
    Number: Optional[str] = None
    Tags: list[UserTag]
    Type: Optional[PeerType] = None


class SetRouteRequest(Schema):
    Id: int
    Routes: list[SetRoute]


class XTelegramAuth(Schema):
    ApiHash: str
    ApiId: str
    RequiredFields: list[KeyValuePair_2OfString_String]
    Session: str
    TrunkNo: str


class InboundRule(Schema):
    AlterDestinationDuringHolidays: Optional[bool] = None
    AlterDestinationDuringOutOfOfficeHours: Optional[bool] = None
    CallType: Optional[RuleCallTypeType] = None
    Condition: Optional[RuleConditionType] = None
    CustomData: Optional[str] = None
    Data: Optional[str] = None
    HolidaysDestination: Optional[Destination] = None
    Hours: Optional[Schedule] = None
    Id: int
    OfficeHoursDestination: Optional[Destination] = None
    OutOfOfficeHoursDestination: Optional[Destination] = None
    RuleName: Optional[str] = None
    TrunkDN: Optional[Peer] = None


class Gateway(Schema):
    Codecs: Optional[list[str]] = None
    DeliverAudio: Optional[bool] = None
    DestNumberInRemotePartyIDCalled: Optional[bool] = None
    DestNumberInRequestLineURI: Optional[bool] = None
    DestNumberInTo: Optional[bool] = None
    Host: Optional[str] = None
    Id: Optional[int] = None
    InboundParams: Optional[list[GatewayParameterBinding]] = None
    Internal: Optional[bool] = None
    IPInRegistrationContact: Optional[IPInRegistrationContactType] = None
    Lines: Optional[int] = None
    MatchingStrategy: Optional[MatchingStrategyType] = None
    Name: Optional[str] = None
    OutboundCallerID: Optional[str] = None
    OutboundParams: Optional[list[GatewayParameterBinding]] = None
    Port: Optional[int] = None
    ProxyHost: Optional[str] = None
    ProxyPort: Optional[int] = None
    RequireRegistrationFor: Optional[RequireRegistrationForType] = None
    SourceIdentification: Optional[list[GatewayParameterBinding]] = None
    SpecifiedIPForRegistrationContact: Optional[str] = None
    SRTPMode: Optional[SRTPModeType] = None
    SupportReinvite: Optional[bool] = None
    SupportReplaces: Optional[bool] = None
    TemplateFilename: Optional[str] = None
    TimeBetweenReg: Optional[int] = None
    Type: GatewayType
    UseIPInContact: Optional[bool] = None
    VariableChoices: Optional[list[Choice]] = None


class Trunk(Schema):
    AuthID: Optional[str] = None
    AuthPassword: Optional[str] = None
    ConfigurationIssue: Optional[str] = None
    DidNumbers: Optional[list[str]] = None
    Direction: Optional[DirectionType] = None
    DisableVideo: Optional[bool] = None
    E164CountryCode: Optional[str] = None
    E164ProcessIncomingNumber: Optional[bool] = None
    EnableInboundCalls: Optional[bool] = None
    EnableOutboundCalls: Optional[bool] = None
    ExternalNumber: Optional[str] = None
    gateway: Optional[Gateway] = Field(None, alias="Gateway")
    Groups: list[UserGroup] = Field(default_factory=list)
    Id: int
    InCIDFormatting: Optional[list[CIDFormatting]] = None
    IPRestriction: Optional[TypeOfIPDestriction] = None
    IsOnline: Optional[bool] = None
    IsWebmeetingBridge: Optional[bool] = None
    Messaging: Optional[TrunkMessaging] = None
    Number: Optional[str] = None
    OutboundCallerID: Optional[str] = None
    OutCIDFormatting: Optional[list[CIDFormatting]] = None
    PublicInfoGroups: Optional[list[str]] = None
    PublicIPinSIP: Optional[str] = None
    PublishInfo: Optional[bool] = None
    ReceiveExtensions: Optional[list[str]] = None
    ReceiveInfo: Optional[bool] = None
    RemoteMyPhoneUriHost: Optional[str] = None
    RemotePBXPreffix: Optional[str] = None
    RoutingRules: list[InboundRule] = Field(default_factory=list)
    SecondaryRegistrar: Optional[str] = None
    SeparateAuthId: Optional[str] = None
    SimultaneousCalls: Optional[int] = None
    TransportRestriction: Optional[TypeOfTransportRestriction] = None
    TunnelEnabled: Optional[bool] = None
    TunnelRemoteAddr: Optional[str] = None
    TunnelRemotePort: Optional[int] = None
    UseSeparateAuthId: Optional[bool] = None


class Country(Schema):
    Continent: Optional[str] = None
    CountryCode: Optional[str] = None
    CountryCodes: Optional[list[str]] = None
    DownloadUrl: Optional[str] = None
    ErpCode: Optional[str] = None
    ExitCode: Optional[str] = None
    Name: str
    ParentErpCode: Optional[str] = None
    StunServer: Optional[str] = None
    VoicemailNo: Optional[str] = None
    WebMeetingZone: Optional[str] = None


class RegistrarFxs(Schema):
    InterfaceLink: str
    MacAddress: str


class FxsTemplate(Schema):
    AllowedNetConfigs: Optional[list[str]] = None
    AllowSSLProvisioning: Optional[bool] = None
    Brand: str
    Content: Optional[str] = None
    DeviceType: DeviceType
    Id: str
    IsCustom: bool
    Languages: Optional[list[str]] = None
    Models: list[FxsModel]
    NumberOfExtensions: int
    TemplateType: TemplateType
    TimeZones: Optional[list[str]] = None
    URL: str
    Variables: list[FxsVariable]


class Fxs(Schema):
    Brand: Optional[str] = None
    Codecs: Optional[list[str]] = None
    FxsLineCount: Optional[int] = None
    FxsLines: Optional[list[DeviceLine]] = None
    Group: Optional[str] = None
    Language: Optional[str] = None
    MacAddress: str
    Model: Optional[str] = None
    ModelName: Optional[str] = None
    Name: Optional[str] = None
    Password: Optional[str] = None
    Provisioning: Optional[FxsProvisioning] = None
    Registered: Optional[RegistrarFxs] = None
    Secret: Optional[str] = None
    Template: Optional[FxsTemplate] = None
    TimeZone: Optional[str] = None
    Variables: Optional[list[Variable]] = None


class LicenseStatus(Schema):
    Activated: Optional[bool] = None
    AdminEMail: Optional[str] = None
    EMail: Optional[str] = None
    ExpirationDate: Optional[datetime]
    FQDN: Optional[str] = None
    HasNotRunningServices: Optional[bool] = None
    IpV4: Optional[str] = None
    LicenseActive: Optional[bool] = None
    LicenseKey: Optional[str] = None
    MaintenanceExpiresAt: Optional[datetime]
    MaxSimCalls: Optional[int] = None
    NetworkPorts: Optional[str] = None
    ProductCode: str
    ResellerName: Optional[str] = None
    Support: Optional[bool] = None
    Version: Optional[str] = None


class ResellerInfo(Schema):
    Id: Optional[str] = None
    Name: Optional[str] = None


class PromptSet(Schema):
    CultureCode: Optional[str] = None
    Description: Optional[str] = None
    Folder: Optional[str] = None
    Id: int
    LanguageCode: Optional[str] = None
    Prompts: list[Prompt]
    PromptSetName: Optional[str] = None
    prompt_set_type: Optional[PromptSetType] = Field(None, alias="PromptSetType")
    UseAlternateNumberPronunciation: Optional[bool] = None
    Version: Optional[str] = None


class CustomPrompt(Schema):
    CanBeDeleted: bool
    DisplayName: str
    FileLink: str
    Filename: str
    Fullpath: Optional[str] = None
    PromptType: PromptType


class Property(Schema):
    Description: Optional[str] = None
    Name: str
    Value: str


class Weblink(Schema):
    Advanced: Optional[LiveChatAdvancedSettings] = None
    CallsEnabled: Optional[bool] = None
    ChatBox: Optional[LiveChatBox] = None
    ChatEnabled: Optional[bool] = None
    DefaultRecord: Optional[bool] = None
    DN: Optional[Peer] = None
    General: Optional[GeneralLiveChatSettings] = None
    Group: Optional[str] = None
    Hidden: Optional[bool] = None
    Id: Optional[int] = None
    Link: str
    MeetingEnabled: Optional[bool] = None
    Name: Optional[str] = None
    Styling: Optional[LiveChatStyling] = None
    Translations: Optional[WebsiteLinksTranslations] = None
    Website: Optional[list[str]] = None


class ChatLinkNameValidation(Schema):
    FriendlyName: str
    Pair: str


class UpdateSettings(Schema):
    AutoUpdateEnabled: Optional[bool] = None
    Schedule: Optional[BackupSchedule] = None


class UpdateList(Schema):
    Entries: Optional[list[UpdateItem]] = None
    IsMaintananceExpired: Optional[bool] = None
    Key: UUID = None
    LastSuccessfulUpdate: Optional[datetime]


class InstallUpdates(Schema):
    Entries: list[UUID]
    Key: UUID


class UpdatesStats(Schema):
    PerPage: Optional[list[CategoryUpdate]] = None
    TcxUpdate: Optional[list[CategoryUpdate]] = None


class Parking(Schema):
    Groups: list[UserGroup]
    Id: int
    Number: Optional[str] = None


class Backups(Schema):
    CreationTime: Optional[datetime]
    DownloadLink: str
    FileName: str
    Size: Optional[int] = None


class CreateBackup(Schema):
    Contents: Optional[BackupContents] = None
    Name: str = Field(max_length=50)


class BackupExtras(Schema):
    Footprint: Optional[int] = None
    IsEncrypted: Optional[bool] = None
    Version: str


class BackupSettings(Schema):
    Contents: Optional[BackupContents] = None
    Rotation: Optional[int] = None
    Schedule: Optional[BackupSchedule] = None
    ScheduleEnabled: Optional[bool] = None


class BackupRepositorySettings(Schema):
    Location: Optional[LocationSettings] = None


class BackupFailoverSettings(Schema):
    Condition: Optional[FailoverCondition] = None
    Enabled: Optional[bool] = None
    Interval: Optional[int] = None
    Mode: Optional[FailoverMode] = None
    PostStartScript: Optional[str] = None
    PreStartScript: Optional[str] = None
    RemoteServer: Optional[str] = None
    TestSIPServer: Optional[bool] = None
    TestTunnel: Optional[bool] = None
    TestWebServer: Optional[bool] = None


class FailoverScriptFile(Schema):
    Filename: str


class RestoreSettings(Schema):
    EncryptBackup: Optional[bool] = None
    EncryptBackupPassword: Optional[str] = None
    Schedule: Optional[BackupSchedule] = None
    ScheduleEnabled: Optional[bool] = None


class Sbc(Schema):
    DisplayName: str
    Group: Optional[str] = None
    HasConnection: Optional[bool] = None
    LocalIPv4: Optional[str] = None
    Name: str = Field(max_length=12)
    Password: str
    PhoneMAC: Optional[str] = None
    PhoneUserId: Optional[int] = None
    ProvisionLink: Optional[str] = None


class CallHistoryView(Schema):
    CallAnswered: bool
    CallTime: str
    DstCallerNumber: Optional[str] = None
    DstDisplayName: Optional[str] = None
    DstDn: Optional[str] = None
    DstDnType: int
    DstExtendedDisplayName: Optional[str] = None
    DstExternal: bool
    DstId: int
    DstInternal: bool
    DstParticipantId: int
    DstRecId: Optional[int] = None
    SegmentActionId: int
    SegmentEndTime: datetime
    SegmentId: int
    SegmentStartTime: datetime
    SegmentType: int
    SrcCallerNumber: Optional[str] = None
    SrcDisplayName: Optional[str] = None
    SrcDn: Optional[str] = None
    SrcDnType: int
    SrcExtendedDisplayName: Optional[str] = None
    SrcExternal: bool
    SrcId: int
    SrcInternal: bool
    SrcParticipantId: int
    SrcRecId: Optional[int] = None


class ChatHistoryView(Schema):
    ChatName: Optional[str] = None
    ConversationId: int
    FromName: Optional[str] = None
    FromNo: Optional[str] = None
    IsExternal: bool
    Message: Optional[str] = None
    ParticipantEmail: Optional[str] = None
    ParticipantIp: Optional[str] = None
    ParticipantPhone: Optional[str] = None
    ParticipantsGroupsArray: Optional[list[str]] = None
    ProviderName: Optional[str] = None
    ProviderType: Optional[ChatType] = None
    QueueNumber: Optional[str] = None
    Source: Optional[str] = None
    TimeSent: datetime


class ChatMessagesHistoryView(Schema):
    ConversationId: int
    IsExternal: bool
    Message: Optional[str] = None
    MessageId: int
    ParticipantsGroupsArray: Optional[list[str]] = None
    QueueNumber: Optional[str] = None
    Recipients: Optional[str] = None
    SenderParticipantEmail: Optional[str] = None
    SenderParticipantIp: Optional[str] = None
    SenderParticipantName: Optional[str] = None
    SenderParticipantNo: Optional[str] = None
    SenderParticipantPbx: Optional[str] = None
    SenderParticipantPhone: Optional[str] = None
    TimeSent: datetime


class RingGroupStatistics(Schema):
    RingGroupAnsweredCount: Optional[int] = None
    RingGroupDisplayName: Optional[str] = None
    RingGroupDn: str
    RingGroupReceivedCount: Optional[int] = None


class ExtensionsStatisticsByRingGroups(Schema):
    ExtensionAnsweredCount: Optional[int] = None
    ExtensionDisplayName: Optional[str] = None
    ExtensionDn: str
    RingGroupDisplayName: Optional[str] = None
    RingGroupDn: str


class CallLogData(Schema):
    ActionDnCallerId: Optional[str] = None
    ActionDnDisplayName: Optional[str] = None
    actionDnDn: Optional[str] = None
    ActionDnType: Optional[int] = None
    ActionType: Optional[int] = None
    Answered: Optional[bool] = None
    CallCost: Optional[Decimal] = None
    CallId: int
    DestinationCallerId: Optional[str] = None
    DestinationDisplayName: Optional[str] = None
    DestinationDn: Optional[str] = None
    DestinationType: Optional[int] = None
    DstRecId: Optional[int] = None
    Indent: Optional[int] = None
    QualityReport: Optional[bool] = None
    Reason: Optional[str] = None
    RecordingUrl: Optional[str] = None
    RingingDuration: Optional[str] = None
    SegmentId: Optional[int] = None
    SourceCallerId: Optional[str] = None
    SourceDisplayName: Optional[str] = None
    SourceDn: Optional[str] = None
    SourceType: Optional[int] = None
    SrcRecId: Optional[int] = None
    StartTime: datetime
    SubrowDescNumber: Optional[int] = None
    TalkingDuration: Optional[str] = None


class QualityReport(Schema):
    MOS: Optional[float | ReferenceNumeric] = None
    OverallScore: Optional[int] = None
    Party1: Optional[QualityParty] = None
    Party2: Optional[QualityParty] = None
    Summary: Optional[int] = None
    Transcoding: Optional[bool] = None


class ExtensionStatistics(Schema):
    DisplayName: Optional[str] = None
    Dn: str
    InboundAnsweredCount: Optional[int] = None
    InboundAnsweredTalkingDur: Optional[str] = None
    InboundUnansweredCount: Optional[int] = None
    OutboundAnsweredCount: Optional[int] = None
    OutboundAnsweredTalkingDur: Optional[str] = None
    OutboundUnansweredCount: Optional[int] = None


class ReportExtensionStatisticsByGroup(Schema):
    DisplayName: Optional[str] = None
    Dn: str
    InboundAnsweredCount: Optional[int] = None
    InboundAnsweredTalkingDur: Optional[str] = None
    InboundUnansweredCount: Optional[int] = None
    OutboundAnsweredCount: Optional[int] = None
    OutboundAnsweredTalkingDur: Optional[str] = None
    OutboundUnansweredCount: Optional[int] = None


class CallCostByExtensionGroup(Schema):
    BillingCost: Optional[Decimal] = None
    CallType: Optional[str] = None
    DstDn: Optional[str] = None
    DstDnClass: Optional[int] = None
    GroupName: Optional[str] = None
    IsAnswered: Optional[bool] = None
    RingingDur: Optional[str] = None
    SegId: int
    SrcDisplayName: Optional[str] = None
    SrcDn: Optional[str] = None
    StartTime: Optional[datetime]
    TalkingDur: Optional[str] = None


class QueuePerformanceOverview(Schema):
    ExtensionAnsweredCount: Optional[int] = None
    ExtensionDisplayName: Optional[str] = None
    ExtensionDn: str
    ExtensionDroppedCount: Optional[int] = None
    QueueAnsweredCount: Optional[int] = None
    QueueDisplayName: str
    QueueDn: Optional[str] = None
    QueueReceivedCount: Optional[int] = None
    TalkTime: Optional[str] = None


class QueuePerformanceTotals(Schema):
    ExtensionAnsweredCount: Optional[int] = None
    ExtensionDroppedCount: Optional[int] = None
    QueueDisplayName: Optional[str] = None
    QueueDn: str
    QueueReceivedCount: Optional[int] = None


class TeamQueueGeneralStatistics(Schema):
    AgentsInQueueCount: Optional[int] = None
    AnsweredCount: Optional[int] = None
    AvgTalkTime: Optional[str] = None
    Dn: Optional[str] = None
    QueueDnNumber: str
    ReceivedCount: Optional[int] = None
    TotalTalkTime: Optional[str] = None


class DetailedQueueStatistics(Schema):
    AnsweredCount: Optional[int] = None
    AvgRingTime: Optional[str] = None
    AvgTalkTime: Optional[str] = None
    CallbacksCount: Optional[int] = None
    CallsCount: Optional[int] = None
    QueueDn: Optional[str] = None
    QueueDnNumber: str
    RingTime: Optional[str] = None
    TalkTime: Optional[str] = None


class AbandonedQueueCalls(Schema):
    CallerId: Optional[str] = None
    CallHistoryId: Optional[str] = None
    CallTime: Optional[datetime]
    CallTimeForCsv: Optional[datetime]
    ExtensionDisplayName: Optional[str] = None
    ExtensionDn: Optional[str] = None
    IsLoggedIn: Optional[bool] = None
    PollingAttempts: Optional[int] = None
    QueueDisplayName: Optional[str] = None
    QueueDn: str
    WaitTime: Optional[str] = None


class QueueAnsweredCallsByWaitTime(Schema):
    AnsweredTime: datetime
    CallTime: datetime
    Destination: str
    Dn: str
    DnNumber: Optional[str] = None
    RingTime: Optional[str] = None
    Source: str


class QueueCallbacks(Schema):
    CallbacksCount: Optional[int] = None
    Dn: Optional[str] = None
    FailCallbacksCount: Optional[int] = None
    QueueDnNumber: str
    ReceivedCount: Optional[int] = None


class AgentsInQueueStatistics(Schema):
    AnsweredCount: Optional[int] = None
    AnsweredPercent: Optional[int] = None
    AnsweredPerHourCount: Optional[int] = None
    AvgRingTime: Optional[str] = None
    AvgTalkTime: Optional[str] = None
    Dn: str
    DnDisplayName: Optional[str] = None
    LoggedInTime: Optional[str] = None
    LostCount: Optional[int] = None
    Queue: Optional[str] = None
    QueueDisplayName: Optional[str] = None
    RingTime: Optional[str] = None
    TalkTime: Optional[str] = None


class QueueFailedCallbacks(Schema):
    CallbackNo: str
    CallTime: datetime
    Dn: str
    QueueDnNumber: Optional[str] = None
    RingTime: Optional[str] = None


class StatisticSla(Schema):
    BadSlaCallsCount: Optional[int] = None
    Dn: Optional[str] = None
    QueueDnNumber: str
    ReceivedCount: Optional[int] = None


class BreachesSla(Schema):
    CallerId: str
    CallTime: datetime
    Queue: str
    QueueDnNumber: Optional[str] = None
    WaitingTime: Optional[str] = None


class CallFlowApp(Schema):
    CompilationLastSuccess: Optional[datetime]
    CompilationResult: Optional[str] = None
    CompilationSucceeded: Optional[bool] = None
    Groups: list[UserGroup]
    Id: int
    InvalidScript: Optional[bool] = None
    IsRegistered: Optional[bool] = None
    Name: Optional[str] = None
    Number: Optional[str] = None
    ProjectName: Optional[str] = None
    RejectedCode: Optional[str] = None
    ScriptCode: Optional[str] = None
    ScriptName: Optional[str] = None


class QueueChatPerformance(Schema):
    AbandonedCount: Optional[int] = None
    AnsweredCount: Optional[int] = None
    IncomingCount: Optional[int] = None
    QuantityAgents: Optional[int] = None
    Queue: str
    QueueDisplayName: Optional[str] = None


class QueueAgentsChatStatistics(Schema):
    AnsweredCount: Optional[int] = None
    DealtWithCount: Optional[int] = None
    Dn: str
    DnDisplayName: Optional[str] = None
    Queue: str
    QueueDisplayName: Optional[str] = None


class QueueAgentsChatStatisticsTotals(Schema):
    AnsweredCount: Optional[int] = None
    DealtWithCount: Optional[int] = None
    Queue: str
    QueueDisplayName: Optional[str] = None


class AbandonedChatsStatistics(Schema):
    ChatId: int
    DateOfRequest: datetime
    ParticipantEmail: str
    ParticipantMessage: str
    ParticipantName: Optional[str] = None
    ParticipantNumber: str
    QueueDisplayName: Optional[str] = None
    QueueNo: str
    ReasonForAbandoned: Optional[str] = None
    ReasonForDealtWith: Optional[str] = None
    Source: str


class AgentLoginHistory(Schema):
    Agent: str
    AgentNo: str
    Day: Optional[datetime]
    LoggedInDayInterval: Optional[str] = None
    loggedInDt: Optional[datetime]
    LoggedInInterval: Optional[str] = None
    LoggedInTotalInterval: Optional[str] = None
    LoggedOutDt: Optional[datetime]
    QueueNo: str
    TalkingDayInterval: Optional[str] = None
    TalkingInterval: Optional[str] = None
    TalkingTotalInterval: Optional[str] = None


class AuditLog(Schema):
    Action: Optional[int] = None
    Id: int
    Ip: Optional[str] = None
    NewData: Optional[str] = None
    ObjectName: Optional[str] = None
    ObjectType: Optional[int] = None
    PrevData: Optional[str] = None
    Source: Optional[int] = None
    Timestamp: Optional[datetime]
    UserName: Optional[str] = None


class InboundRuleReport(Schema):
    DID: Optional[str] = None
    Id: int
    InOfficeRouting: Optional[str] = None
    OutOfficeRouting: Optional[str] = None
    RuleName: Optional[str] = None
    Trunk: Optional[str] = None


class CrmTemplate(Schema):
    Authentication: Optional[CrmAuthentication] = None
    Name: str
    Parameters: Optional[list[CrmParameter]] = None


class NetworkSettings(Schema):
    AllowSourceAsOutbound: Optional[bool] = None
    DirectSIPAllowExternal: Optional[bool] = None
    DirectSIPLocalDomain: Optional[str] = None
    FirewallKeepAlive: Optional[bool] = None
    FirewallKeepAliveInterval: Optional[int] = None
    Id: str
    IpV6BindingEnabled: Optional[bool] = None
    PbxPublicFQDN: Optional[str] = None
    PublicInterface: Optional[str] = None
    PublicStaticIP: Optional[str] = None
    SipPort: Optional[int] = None
    StunDisabled: Optional[bool] = None
    StunPrimaryHost: Optional[str] = None
    StunPrimaryPort: Optional[int] = None
    StunQuery: Optional[int] = None
    StunSecondaryHost: Optional[str] = None
    StunSecondaryPort: Optional[int] = None
    StunThirdHost: Optional[str] = None
    StunThirdPort: Optional[int] = None
    TunnelPort: Optional[int] = None


class CDRSettings(Schema):
    Enabled: Optional[bool] = None
    EnabledFields: Optional[list[CDRSettingsField]] = None
    LogSize: Optional[int] = None
    LogType: Optional[TypeOfCDRLog] = None
    PossibleFields: Optional[list[str]] = None
    RemoveCommaDelimiters: Optional[bool] = None
    SocketIpAddress: Optional[str] = None
    SocketPort: Optional[int] = None


class CallCostSettings(Schema):
    CountryName: Optional[str] = None
    Id: int
    Invalid: Optional[bool] = None
    Prefix: Optional[str] = None
    Rate: Optional[float | ReferenceNumeric] = None
    ReadOnly: Optional[bool] = None


class PhoneLogo(Schema):
    DisplayName: Optional[str] = None
    Filename: str


class TimeReportData(Schema):
    XValue: datetime
    YValue1: Optional[int] = None
    YValue2: Optional[int] = None


class ReportGroup(Schema):
    GroupID: int
    GroupName: Optional[str] = None


class EventLog(Schema):
    EventId: Optional[int] = None
    Group: Optional[str] = None
    GroupName: Optional[str] = None
    Id: int
    Message: Optional[str] = None
    Params: Optional[list[str]] = None
    Source: Optional[str] = None
    TimeGenerated: Optional[datetime]
    Type: Optional[EventLogType] = None


class ServiceInfo(Schema):
    CpuUsage: Optional[int] = None
    DisplayName: Optional[str] = None
    HandleCount: Optional[int] = None
    MemoryUsed: Optional[int] = None
    Name: str
    RestartEnabled: Optional[bool] = None
    StartStopEnabled: Optional[bool] = None
    Status: Optional[ServiceStatus] = None
    ThreadCount: Optional[int] = None


class XServiceManageOptions(Schema):
    ServiceNames: Optional[list[str]] = None


class FirewallState(Schema):
    Html: Optional[str] = None
    Id: str
    Running: Optional[bool] = None
    Stopping: Optional[bool] = None


class Microsoft365Integration(Schema):
    AdUsers: Optional[ADUsersSyncConfiguration] = None
    ApplicationId: str
    Id: int
    SharedMailboxesSync: Optional[UsersSyncConfiguration] = None


class Microsoft365User(Schema):
    Email: str
    Id: str
    Name: str


class Microsoft365SubscriptionTestResult(Schema):
    ExceptionMessage: Optional[str] = None
    Fqdn: Optional[str] = None
    IsSubscriptionAvailable: Optional[bool] = None


class Microsoft365Status(Schema):
    ApplicationId: Optional[str] = None
    ExceptionMessage: Optional[str] = None
    ProvisionUrl: Optional[str] = None


class Microsoft365UsersPage(Schema):
    Total: Optional[int] = None
    Users: Optional[list[Microsoft365User]] = None


class UsersRequestOptions(Schema):
    Count: int
    Search: Optional[str] = None
    Start: int
    TypeOfUser: TypeOfUser


class Microsoft365TeamsIntegration(Schema):
    AreaCode: Optional[str] = None
    DialPlanCode: Optional[str] = None
    Enabled: Optional[bool] = None
    Id: int
    IsDynamicIP: Optional[bool] = None
    IsNativeFQDN: Optional[bool] = None
    SbcCertificate: Optional[str] = None
    SbcCertificateExpirationDate: Optional[str] = None
    SbcCertificateFile: Optional[str] = None
    SbcFQDN: Optional[str] = None
    SbcPrivateKey: Optional[str] = None
    SbcPrivateKeyFile: Optional[str] = None
    SecureSipEnabled: Optional[bool] = None
    SipDomain: Optional[str] = None
    TlsPortForNativeFQDN: Optional[int] = None
    TlsPortForNonNativeFQDN: Optional[int] = None


class VoicemailSettings(Schema):
    AutoDeleteDays: Optional[int] = None
    AutoDeleteEnabled: Optional[bool] = None
    Extension: Optional[str] = None
    Id: int
    MinDuration: Optional[int] = None
    Quota: Optional[int] = None
    SendEmailQuotaEnabled: Optional[bool] = None
    SendEmailQuotaPercentage: Optional[int] = None
    TranscribeEnabled: Optional[bool] = None
    TranscribeLanguage: Optional[str] = None
    TranscribeLevel: Optional[TranscriptionLevel] = None
    TranscribeRegion: Optional[str] = None
    TranscribeSecretKey: Optional[str] = None
    UsedSpace: Optional[int] = None


class LanguageItem(Schema):
    Code: Optional[str] = None
    Name: Optional[str] = None


class ConferenceSettings(Schema):
    ApiKey: Optional[str] = None
    AutoCallParticipants: Optional[bool] = None
    EnablePin: Optional[bool] = None
    Extension: Optional[str] = None
    ExternalNumbers: Optional[str] = Field(default=None, max_length=500)
    Id: int
    LogoPath: Optional[str] = None
    MusicOnHold: Optional[str] = None
    PinNumber: Optional[str] = None
    Zone: Optional[str] = None


class NotificationSettings(Schema):
    CanEditEmailAddresses: Optional[bool] = None
    CanEditMailServerType: Optional[bool] = None
    EmailAddresses: Optional[str] = None
    FakeId: str
    MailAddress: Optional[str] = None
    MailPassword: Optional[str] = None
    MailServer: Optional[str] = None
    mail_server_type: Optional[MailServerType] = Field(default=None, alias="MailServerType")
    MailSslEnabled: Optional[bool] = None
    MailUser: Optional[str] = None
    NotifyCallDenied: Optional[bool] = None
    NotifyEmergencyNumberDialed: Optional[bool] = None
    NotifyExtensionAdded: Optional[bool] = None
    NotifyIPBlocked: Optional[bool] = None
    NotifyLicenseLimit: Optional[bool] = None
    NotifyNetworkError: Optional[bool] = None
    NotifyRequestAntiHacked: Optional[bool] = None
    NotifyServiceStopped: Optional[bool] = None
    NotifyStorageLimit: Optional[bool] = None
    NotifySTUNError: Optional[bool] = None
    NotifySuccessScheduledBackups: Optional[bool] = None
    NotifySystemOwners: Optional[bool] = None
    NotifyTrunkError: Optional[bool] = None
    NotifyTrunkFailover: Optional[bool] = None
    NotifyTrunkStatusChanged: Optional[bool] = None
    NotifyUpdatesAvailable: Optional[bool] = None
    NotifyWhenRecordingsQuotaReached: Optional[bool] = None
    NotifyWhenVoicemailQuotaReached: Optional[bool] = None
    RecordingsQuotaPercentage: Optional[int] = None
    VoicemailQuotaPercentage: Optional[int] = None


class TestResult(Schema):
    Error: Optional[str] = None
    Parameters: Optional[list[str]] = None
    Success: Optional[bool] = None


class EmailTemplate(Schema):
    Body: str
    From: Optional[str] = None
    IsConference: Optional[bool] = None
    IsDefault: Optional[bool] = None
    Lang: Optional[str] = None
    Name: Optional[str] = None
    Subject: Optional[str] = None
    TemplatePath: str


class HotelServices(Schema):
    Enabled: Optional[bool] = None
    HotelGroups: Optional[list[str]] = None
    IntegrationType: Optional[PmsIntegrationType] = None
    IpAddress: Optional[str] = None
    NoAnswerDestination: Optional[Destination] = None
    NoAnswerTimeout: Optional[int] = None
    Port: Optional[int] = None


class FirmwareState(Schema):
    Count: Optional[int] = None
    FileNames: Optional[list[str]] = None
    Id: str
    TotalSize: Optional[int] = None


class SystemStatus(Schema):
    Activated: Optional[bool] = None
    AutoUpdateEnabled: Optional[bool] = None
    AvailableLocalIps: Optional[str] = None
    BackupScheduled: Optional[bool] = None
    BlacklistedIpCount: Optional[int] = None
    CallsActive: Optional[int] = None
    CpuUsage: Optional[int] = None
    CurrentLocalIp: Optional[str] = None
    DBMaintenanceInProgress: Optional[bool] = None
    DiskUsage: Optional[int] = None
    ExpirationDate: Optional[datetime]
    ExtensionsRegistered: Optional[int] = None
    ExtensionsTotal: Optional[int] = None
    FQDN: Optional[str] = None
    FreeDiskSpace: Optional[int] = None
    FreePhysicalMemory: Optional[int] = None
    FreeVirtualMemory: Optional[int] = None
    HasNotRunningServices: Optional[bool] = None
    HasUnregisteredSystemExtensions: Optional[bool] = None
    Id: int
    Ip: Optional[str] = None
    IpV4: Optional[str] = None
    IpV6: Optional[str] = None
    IsAuditLogEnabled: Optional[bool] = None
    IsChatLogEnabled: Optional[bool] = None
    IsRecordingArchiveEnabled: Optional[bool] = None
    IsSpla: Optional[bool] = None
    LastBackupDateTime: Optional[datetime]
    LastCheckForUpdates: Optional[datetime]
    LastSuccessfulUpdate: Optional[datetime]
    LicenseActive: Optional[bool] = None
    LicenseKey: Optional[str] = None
    LocalIpValid: Optional[bool] = None
    MaintenanceExpiresAt: Optional[datetime]
    MaxSimCalls: Optional[int] = None
    MaxSimMeetingParticipants: Optional[int] = None
    OS: Optional[XOperatingSystemType] = None
    OutboundRules: Optional[int] = None
    OwnPush: Optional[bool] = None
    PhysicalMemoryUsage: Optional[int] = None
    ProductCode: Optional[str] = None
    RecordingQuota: Optional[int] = None
    RecordingQuotaReached: Optional[bool] = None
    RecordingStopped: Optional[bool] = None
    RecordingUsedSpace: Optional[int] = None
    ResellerName: Optional[str] = None
    SpliDNSConversionState: Optional[SplitDNSConversionState] = None
    SplitDNSConversionRequired: Optional[bool] = None
    Support: Optional[bool] = None
    TotalDiskSpace: Optional[int] = None
    TotalPhysicalMemory: Optional[int] = None
    TotalVirtualMemory: Optional[int] = None
    TrunksRegistered: Optional[int] = None
    TrunksTotal: Optional[int] = None
    Version: Optional[str] = None
    VirtualMemoryUsage: Optional[int] = None
    WebMeetingFQDN: Optional[str] = None
    WebMeetingStatus: Optional[str] = None


class SystemExtensionStatus(Schema):
    IsRegistered: Optional[bool] = None
    Name: Optional[str] = None
    Number: Optional[str] = None
    Type: Optional[str] = None


class SystemDatabaseInformation(Schema):
    CallHistoryCount: Optional[int] = None
    ChatMessagesCount: Optional[int] = None
    Id: Optional[int] = None
    TodayOutboundCallsCount: Optional[int] = None


class VersionUpdateType(Schema):
    Type: Optional[UpdateType] = None


class SystemHealthStatus(Schema):
    CustomTemplatesCount: Optional[int] = None
    Firewall: Optional[bool] = None
    Id: Optional[int] = None
    Phones: Optional[bool] = None
    Trunks: Optional[bool] = None
    UnsupportedFirmwaresCount: Optional[int] = None


class Playlist(Schema):
    AutoGain: Optional[bool] = None
    Files: Optional[list[str]] = None
    MaxVolumePercent: Optional[int] = None
    Name: str
    PromptName: Optional[str] = None
    RepositoryPath: Optional[str] = None
    Shuffle: Optional[bool] = None


class FaxServerSettings(Schema):
    AuthId: Optional[str] = None
    AuthPassword: Optional[str] = None
    Email: Optional[str] = None
    FaxServerId: Optional[int] = None
    G711ToT38Fallback: Optional[bool] = None
    Number: str


class Fax(Schema):
    AuthID: Optional[str] = None
    AuthPassword: Optional[str] = None
    FaxServer: Optional[bool] = None
    Groups: list[UserGroup]
    Id: int
    Number: Optional[str] = None
    OutboundCallerId: Optional[str] = None


class PurgeSettings(Schema):
    All: bool
    Start: Optional[datetime]
    Stop: Optional[datetime]


class Codec(Schema):
    Id: int
    Name: Optional[str] = None
    RfcName: Optional[str] = None


class VoipProvider(Schema):
    Countries: Optional[list[str]] = None
    Id: str
    Name: str
    Type: TemplateType


class GatewayParameterValue(Schema):
    Description: Optional[str] = None
    Id: int
    Name: Optional[str] = None


class TimeZone(Schema):
    IanaName: str
    Id: str
    Name: str
    WindowsName: str


class GatewayParameter(Schema):
    CanHaveDID: Optional[bool] = None
    Description: Optional[str] = None
    Id: int
    InboundPossibleValues: Optional[list[str]] = None
    Name: Optional[str] = None
    OutboundPossibleValues: Optional[list[str]] = None
    SourceIDPossibleValues: Optional[list[str]] = None


class Defs(Schema):
    Codecs: list[Codec]
    GatewayParameters: list[GatewayParameter]
    GatewayParameterValues: list[GatewayParameterValue]
    Id: int
    TimeZones: list[TimeZone]


class LicenseInfo(Schema):
    Activated: Optional[bool] = None
    AdminEMail: Optional[str] = None
    CompanyName: Optional[str] = None
    ContactName: Optional[str] = None
    CountryCode: Optional[str] = None
    CountryName: Optional[str] = None
    EMail: Optional[str] = None
    ExpirationDate: Optional[datetime]
    LicenseActive: Optional[bool] = None
    LicenseKey: str
    LicenseType: Optional[License] = None
    MaintenanceExpiresAt: Optional[datetime]
    MaxSimCalls: Optional[int] = None
    ProductCode: Optional[str] = None
    ResellerName: Optional[str] = None
    SimMeetingParticipants: Optional[int] = None
    Support: Optional[bool] = None
    Telephone: Optional[str] = None
    Version: Optional[str] = None


class PhoneSettings(Schema):
    AllowCustomQueueRingtones: Optional[bool] = None
    Backlight: Optional[str] = None
    Codecs: Optional[list[str]] = None
    CustomLogo: Optional[str] = None
    CustomQueueRingtones: Optional[list[CustomQueueRingtone]] = None
    DateFormat: Optional[str] = None
    Firmware: Optional[str] = None
    FirmwareLang: Optional[str] = None
    IsLogoCustomizable: Optional[bool] = None
    IsSBC: Optional[bool] = None
    LlDpInfo: Optional[PhoneLldpInfo] = None
    LocalRTPPortEnd: Optional[int] = None
    LocalRTPPortStart: Optional[int] = None
    LocalSipPort: Optional[int] = None
    LogoDescription: Optional[str] = None
    LogoFileExtensionAllowed: Optional[list[str]] = None
    OwnBlfs: Optional[bool] = None
    PhoneLanguage: Optional[str] = None
    PowerLed: Optional[str] = None
    ProvisionExtendedData: Optional[str] = None
    ProvisionType: Optional[ProvType] = None
    QueueRingTone: Optional[str] = None
    RemoteSpmHost: Optional[str] = None
    RemoteSpmPort: Optional[int] = None
    RingTone: Optional[str] = None
    SbcName: Optional[str] = None
    ScreenSaver: Optional[str] = None
    Secret: Optional[str] = None
    Srtp: Optional[str] = None
    TimeFormat: Optional[str] = None
    TimeZone: Optional[str] = None
    VlanInfos: Optional[list[PhoneDeviceVlanInfo]] = None
    XferType: Optional[XferTypeEnum] = None


class Phone(Schema):
    Id: int
    Interface: Optional[str] = None
    MacAddress: Optional[str] = None
    Name: Optional[str] = None
    ProvisioningLinkExt: Optional[str] = None
    ProvisioningLinkLocal: Optional[str] = None
    Settings: Optional[PhoneSettings] = None
    TemplateName: Optional[str] = None


class User(Schema):
    AccessPassword: Optional[str] = None
    AllowLanOnly: Optional[bool] = None
    AllowOwnRecordings: Optional[bool] = None
    AuthID: Optional[str] = None
    AuthPassword: Optional[str] = None
    Blfs: Optional[str] = None
    BreakTime: Optional[Schedule] = None
    CallScreening: Optional[bool] = None
    CallUsEnableChat: Optional[bool] = None
    CallUsEnablePhone: Optional[bool] = None
    CallUsEnableVideo: Optional[bool] = None
    CallUsRequirement: Optional[Authentication] = None
    ClickToCallId: Optional[str] = None
    ContactImage: Optional[str] = None
    CurrentProfileName: Optional[str] = None
    DeskphonePassword: Optional[str] = None
    DisplayName: Optional[str] = None
    EmailAddress: Optional[str] = None
    Enable2FA: Optional[bool] = None
    Enabled: Optional[bool] = None
    EnableHotdesking: Optional[bool] = None
    FirstName: Optional[str] = None
    ForwardingExceptions: list[ExtensionRule] = Field(default_factory=list)
    ForwardingProfiles: list[ForwardingProfile] = Field(default_factory=list)
    GoogleSignInEnabled: Optional[bool] = None
    Greetings: list[Greeting] = Field(default_factory=list)
    Groups: list[UserGroup] = Field(default_factory=list)
    HideInPhonebook: Optional[bool] = None
    HotdeskingAssignment: Optional[str] = None
    Hours: Optional[Schedule] = None
    Id: int
    Internal: Optional[bool] = None
    IsRegistered: Optional[bool] = None
    Language: Optional[str] = None
    LastName: Optional[str] = None
    Mobile: Optional[str] = None
    MS365CalendarEnabled: Optional[bool] = None
    MS365ContactsEnabled: Optional[bool] = None
    MS365SignInEnabled: Optional[bool] = None
    MS365TeamsEnabled: Optional[bool] = None
    MyPhoneAllowDeleteRecordings: Optional[bool] = None
    MyPhoneHideForwardings: Optional[bool] = None
    MyPhonePush: Optional[bool] = None
    MyPhoneShowRecordings: Optional[bool] = None
    Number: Optional[str] = None
    OfficeHoursProps: list[OfficeHoursBits] = Field(default_factory=list)
    OutboundCallerID: Optional[str] = None
    Phones: list[Phone] = Field(default_factory=list)
    PinProtected: Optional[bool] = None
    PinProtectTimeout: Optional[int] = None
    PrimaryGroupId: Optional[int] = None
    PromptSet: Optional[str] = None
    ProvFile: Optional[str] = None
    ProvLink: Optional[str] = None
    RecordCalls: Optional[bool] = None
    RecordExternalCallsOnly: Optional[bool] = None
    Require2FA: Optional[bool] = None
    SendEmailMissedCalls: Optional[bool] = None
    SIPID: Optional[str] = None
    Tags: list[UserTag] = Field(default_factory=list)
    VMDisablePinAuth: Optional[bool] = None
    VMEmailOptions: Optional[VMEmailOptionsType] = None
    VMEnabled: Optional[bool] = None
    VMPIN: Optional[str] = None
    VMPlayCallerID: Optional[bool] = None
    VMPlayMsgDateTime: Optional[VMPlayMsgDateTimeType] = None
    WebMeetingApproveParticipants: Optional[bool] = None
    WebMeetingFriendlyName: Optional[str] = None


class DeviceInfo(Schema):
    Assigned: Optional[bool] = None
    AssignedUser: Optional[str] = None
    DetectedAt: Optional[datetime]
    FirmwareVersion: Optional[str] = None
    Id: int
    InterfaceLink: Optional[str] = None
    MAC: Optional[str] = None
    Model: Optional[str] = None
    NetworkAddress: Optional[str] = None
    NetworkPath: Optional[str] = None
    Parameters: Optional[str] = None
    SbcName: Optional[str] = None
    TemplateName: Optional[str] = None
    UserAgent: Optional[str] = None
    Vendor: Optional[str] = None
    ViaSBC: Optional[bool] = None


class SipDevice(Schema):
    DN: Optional[Peer] = None
    Id: int
    Registrar: Optional[PhoneRegistrar] = None


class GreetingFile(Schema):
    DisplayName: Optional[str] = None
    Filename: str


class NetworkInterface(Schema):
    Id: str


class XLicenseParams(Schema):
    CompanyName: Optional[str] = None
    ContactName: Optional[str] = None
    Country: Optional[str] = None
    Email: Optional[str] = None
    Phone: Optional[str] = None


class SystemParameters(Schema):
    Custom1Name: Optional[str] = None
    Custom2Name: Optional[str] = None
    EmRuleCreationAllowed: Optional[bool] = None
    ENL: Optional[int] = None
    FirstExternalPort: Optional[int] = None
    GlobalACPRMSET: Optional[str] = None
    GlobalLanguage: Optional[str] = None
    HttpPort: Optional[int] = None
    HttpsPort: Optional[int] = None
    IpV6: Optional[str] = None
    Is3CXFQDN: Optional[bool] = None
    IsChatLogEnabled: Optional[bool] = None
    IsHosted: Optional[bool] = None
    IsHosted3CX: Optional[bool] = None
    IsMulticompanyMode: Optional[bool] = None
    IsStaticIp: Optional[bool] = None
    license: Optional[License] = Field(default=None, alias="License")
    PbxExternalHost: Optional[str] = None
    RpsEnabled: Optional[bool] = None
    SipPort: Optional[int] = None
    SipsPort: Optional[int] = None
    StaticIp: Optional[str] = None
    StunIp: Optional[str] = None
    TunnnelPort: Optional[int] = None
    Version: Optional[str] = None
    WebrtcLastPort: Optional[int] = None


class GoogleSettings(Schema):
    ClientId: Optional[str] = None
    ClientSecret: Optional[str] = None
    Id: str
    IsExtensionSignInEnabled: Optional[bool] = None


class ConsoleRestrictions(Schema):
    AccessRestricted: Optional[bool] = None
    Id: str
    IpWhitelist: Optional[list[str]] = None
    MyIpAddress: Optional[str] = None


class MusicOnHoldSettings(Schema):
    Id: int
    MusicOnHold: Optional[str] = None
    MusicOnHold1: Optional[str] = None
    MusicOnHold2: Optional[str] = None
    MusicOnHold3: Optional[str] = None
    MusicOnHold4: Optional[str] = None
    MusicOnHold5: Optional[str] = None
    MusicOnHold6: Optional[str] = None
    MusicOnHold7: Optional[str] = None
    MusicOnHold8: Optional[str] = None
    MusicOnHold9: Optional[str] = None
    MusicOnHoldRandomize: Optional[bool] = None
    MusicOnHoldRandomizePerCall: Optional[bool] = None


class CodecsSettings(Schema):
    ExternalCodecList: Optional[list[str]] = None
    LocalCodecList: Optional[list[str]] = None


class GeneralSettingsForApps(Schema):
    AllowChangePassword: Optional[bool] = None
    EnableChat: Optional[bool] = None
    HideCRMContacts: Optional[bool] = None
    HideInteractionHistory: Optional[bool] = None
    HideSystemExtensions: Optional[bool] = None
    NameOfCustomAvailableStatus: Optional[str] = None
    NameOfCustomOutOfOfficeStatus: Optional[str] = None


class GeneralSettingsForPbx(Schema):
    AllowFwdToExternal: Optional[bool] = None
    BusyMonitor: Optional[bool] = None
    BusyMonitorTimeout: Optional[int] = None
    DisableOutboundCallsOutOfficeHours: Optional[bool] = None
    EnableVMenuOutboundCalls: Optional[bool] = None
    LimitCallPickup: Optional[bool] = None
    OperatorExtension: Optional[str] = None
    PlayBusy: Optional[bool] = None


class CallParkingSettings(Schema):
    AutoPickupEnabled: Optional[bool] = None
    AutoPickupForwardDN: Optional[str] = None
    AutoPickupForwardExternalNumber: Optional[str] = None
    AutoPickupForwardType: Optional[TypeOfAutoPickupForward] = None
    AutoPickupTimeout: Optional[int] = None
    MaximumParkedCalls: Optional[int] = None
    MusicOnHold: Optional[str] = None


class DialCodeSettings(Schema):
    DialCodeBillingCode: Optional[str] = None
    DialCodeHideCallerID: Optional[str] = None
    DialCodeHotdesking: Optional[str] = None
    DialCodeHotelAccess: Optional[str] = None
    DialCodeIntercom: Optional[str] = None
    DialCodeLoggedInQueue: Optional[str] = None
    DialCodeLoggedOutQueue: Optional[str] = None
    DialCodeOutOffice: Optional[str] = None
    DialCodePark: Optional[str] = None
    DialCodePickup: Optional[str] = None
    DialCodeProfileStatus: Optional[str] = None
    DialCodeSetAvailable: Optional[str] = None
    DialCodeSetAway: Optional[str] = None
    DialCodeUnpark: Optional[str] = None
    DialCodeVMail: Optional[str] = None


class E164Settings(Schema):
    AreaCode: Optional[str] = None
    CountryCode: Optional[str] = None
    CountryName: Optional[str] = None
    Enabled: Optional[bool] = None
    InternationalCode: Optional[str] = None
    NationalCode: Optional[str] = None
    Prefix: Optional[str] = None
    RemoveAreaCode: Optional[bool] = None
    RemoveCountryCode: Optional[bool] = None


class CountryCodes(Schema):
    CountryCodes: Optional[list[str]] = None


class SecureSipSettings(Schema):
    Certificate: Optional[str] = None
    PrivateKey: Optional[str] = None


class PhonesSettings(Schema):
    AllowMultiQueueRingtones: Optional[bool] = None
    PhoneAllowMultiFirmwares: Optional[bool] = None
    UseProvisioningSecret: Optional[bool] = None
    UseRpcForLocalPhones: Optional[bool] = None


class OfficeHours(Schema):
    BreakTime: Optional[Schedule] = None
    Hours: Optional[Schedule] = None
    OfficeHolidays: list[Holiday] = Field(default_factory=list)
    SystemLanguage: Optional[str] = None
    TimeZoneId: Optional[str] = None


class PhoneBookSettings(Schema):
    PhoneBookAddQueueName: Optional[TypeOfPhoneBookAddQueueName] = None
    PhoneBookDisplay: Optional[TypeOfPhoneBookDisplay] = None
    ResolvingLength: Optional[int] = None
    ResolvingType: Optional[TypeOfPhoneBookResolving] = None


class EmergencyNotificationsSettings(Schema):
    ChatRecipients: Optional[ChatRecipientsType] = None
    EmergencyDNPrompt: Optional[Peer] = None
    EmergencyPlayPrompt: Optional[str] = None
    SpecifiedList: Optional[str] = None


class CallTypeInfo(Schema):
    DigitsLength: Optional[str] = None
    Prefix: Optional[str] = None


class CallTypesSettings(Schema):
    International: Optional[CallTypeInfo] = None
    Local: Optional[CallTypeInfo] = None
    Mobile: Optional[CallTypeInfo] = None
    National: Optional[CallTypeInfo] = None


class LoggingSettings(Schema):
    KeepLogs: Optional[bool] = None
    KeepLogsDays: Optional[int] = None
    LoggingLevel: Optional[int] = None


class ChatLogSettings(Schema):
    AutoClearMonths: Optional[int] = None
    AutoCloseDays: Optional[int] = None


class CrmSelectableValue(Schema):
    Id: int
    Name: Optional[str] = None


class CrmChoice(Schema):
    Key: str
    Value: Optional[str] = None


class CrmIntegration(Schema):
    Country: Optional[str] = None
    EnabledForDidCalls: Optional[bool] = None
    EnabledForExternalCalls: Optional[bool] = None
    Id: str
    Name: str
    phonebook_priority_options: Optional[PhonebookPriorityOptions] = Field(None, alias="PhonebookPriorityOptions")
    PhonebookSynchronization: Optional[bool] = None
    PossibleValues: list[CrmSelectableValue] = Field(default_factory=list)
    VariableChoices: Optional[list[CrmChoice]] = None


class CrmTestResult(Schema):
    IsError: Optional[bool] = None
    Log: Optional[str] = None
    Message: Optional[str] = None
    SearchResult: Optional[list[CrmContact]] = None


class Warnings(TcxStrEnum):
    WARNINGS_CONTACTS_SPECIFY_NAME_SURNAME_COMPANY = "WARNINGS_CONTACTS_SPECIFY_NAME_SURNAME_COMPANY"
    WARNINGS_CONTACTS_SPECIFY_PHONE_NUMBER = "WARNINGS_CONTACTS_SPECIFY_PHONE_NUMBER"
    WARNINGS_LENGTH_NOT_MORE_50_CHARS = "WARNINGS_LENGTH_NOT_MORE_50_CHARS"
    WARNINGS_LENGTH_NOT_MORE_255_CHARS = "WARNINGS_LENGTH_NOT_MORE_255_CHARS"
    WARNINGSXAPI_LENGTH_NOT_MORE_2048_CHARS = "WARNINGSXAPI_LENGTH_NOT_MORE_2048_CHARS"
    WARNINGSXAPI_INVALID_HEX_CHARACTER = "WARNINGSXAPI_INVALID_HEX_CHARACTER"
    WARNINGS_NO_MORE_NUMBERS_AVAILABLE = "WARNINGS_NO_MORE_NUMBERS_AVAILABLE"
    WARNINGS_ERP_SERVER_ERROR = "WARNINGS_ERP_SERVER_ERROR"
    WARNINGS_LICENSE_NOT_FOUND = "WARNINGS_LICENSE_NOT_FOUND"
    WARNINGS_LIMIT_REACHED = "WARNINGS_LIMIT_REACHED"
    WARNINGSXAPI_INVALID = "WARNINGSXAPI_INVALID"
    WARNINGSXAPI_INVALID_PIN_NUMBER = "WARNINGSXAPI_INVALID_PIN_NUMBER"
    WARNINGSXAPI_NOT_SUPPORTED = "WARNINGSXAPI_NOT_SUPPORTED"
    WARNINGSXAPI_USER_ROLE_DOWNGRADE = "WARNINGSXAPI_USER_ROLE_DOWNGRADE"
    WARNINGS_GROUP_CANNOT_BE_DELETED = "WARNINGS_GROUP_CANNOT_BE_DELETED"
    WARNINGS_CANNOT_BE_DELETED = "WARNINGS_CANNOT_BE_DELETED"
    WARNINGS_GROUP_WITH_MEMBERS_CANNOT_BE_DELETED = "WARNINGS_GROUP_WITH_MEMBERS_CANNOT_BE_DELETED"
    WARNINGSXAPI_OTHER_USER_ROLE_DOWNGRADE = "WARNINGSXAPI_OTHER_USER_ROLE_DOWNGRADE"
    WARNINGSXAPI_INVALID_LICENSE_TYPE = "WARNINGSXAPI_INVALID_LICENSE_TYPE"
    WARNINGSXAPI_INVALID_PASSWORD = "WARNINGSXAPI_INVALID_PASSWORD"
    WARNINGSXAPI_NOT_FOUND = "WARNINGSXAPI_NOT_FOUND"
    WARNINGSXAPI_FILE_NOT_FOUND = "WARNINGSXAPI_FILE_NOT_FOUND"
    WARNINGSXAPI_FILE_NOT_ACCESSIBLE = "WARNINGSXAPI_FILE_NOT_ACCESSIBLE"
    WARNINGSXAPI_REQUIRED = "WARNINGSXAPI_REQUIRED"
    WARNINGSXAPI_CAN_NOT_BE_EMPTY_STRING = "WARNINGSXAPI_CAN_NOT_BE_EMPTY_STRING"
    WARNINGSXAPI_DUPLICATE = "WARNINGSXAPI_DUPLICATE"
    WARNINGSXAPI_ALREADY_IN_USE = "WARNINGSXAPI_ALREADY_IN_USE"
    WARNINGSXAPI_PLAYLIST_IN_USE = "WARNINGSXAPI_PLAYLIST_IN_USE"
    WARNINGSXAPI_OUT_OF_THE_RANGE = "WARNINGSXAPI_OUT_OF_THE_RANGE"
    WARNINGSXAPI_TOO_MANY_PHONES = "WARNINGSXAPI_TOO_MANY_PHONES"
    WARNINGSXAPI_TOO_MANY_SBC = "WARNINGSXAPI_TOO_MANY_SBC"
    WARNINGSXAPI_TOO_MANY_PROMPTS = "WARNINGSXAPI_TOO_MANY_PROMPTS"
    WARNINGSXAPI_OUTBOUND_RULES_LIMIT_REACHED = "WARNINGSXAPI_OUTBOUND_RULES_LIMIT_REACHED"
    WARNINGSXAPI_FORBIDDEN_CHANGE = "WARNINGSXAPI_FORBIDDEN_CHANGE"
    WARNINGS_FAX_SERVER_CANNOT_BE_DELETED = "WARNINGS_FAX_SERVER_CANNOT_BE_DELETED"
    WARNINGS_OPERATOR_CANNOT_BE_DELETED = "WARNINGS_OPERATOR_CANNOT_BE_DELETED"
    WARNINGS_USER_EXTENSION_CANNOT_BE_DELETED = "WARNINGS_USER_EXTENSION_CANNOT_BE_DELETED"
    WARNINGSXAPI_NUMBER_IGNORED = "WARNINGSXAPI_NUMBER_IGNORED"
    WARNINGSXAPI_INVALID_TIMEZONE = "WARNINGSXAPI_INVALID_TIMEZONE"
    WARNINGSXAPI_INVALID_PATH = "WARNINGSXAPI_INVALID_PATH"
    WARNINGSXAPI_PATH_SHOULD_NOT_CONTAIN_SPACES = "WARNINGSXAPI_PATH_SHOULD_NOT_CONTAIN_SPACES"
    WARNINGSXAPI_INVALID_CREDENTIALS = "WARNINGSXAPI_INVALID_CREDENTIALS"
    WARNINGSXAPI_CANNOT_CONNECT_FTP = "WARNINGSXAPI_CANNOT_CONNECT_FTP"
    WARNINGSXAPI_CANNOT_CONNECT_SMB = "WARNINGSXAPI_CANNOT_CONNECT_SMB"
    WARNINGSXAPI_CANNOT_CONNECT_SFTP = "WARNINGSXAPI_CANNOT_CONNECT_SFTP"
    WARNINGSXAPI_CANNOT_CONNECT_GOOGLE_BUCKET = "WARNINGSXAPI_CANNOT_CONNECT_GOOGLE_BUCKET"
    WARNINGSXAPI_PLAYLIST_NO_SOURCE = "WARNINGSXAPI_PLAYLIST_NO_SOURCE"
    WARNINGSXAPI_NO_USERS_IN_TEAMS = "WARNINGSXAPI_NO_USERS_IN_TEAMS"
    WARNINGSXAPI_FILE_FORMAT_IS_INCORRECT = "WARNINGSXAPI_FILE_FORMAT_IS_INCORRECT"
    WARNINGSXAPI_INVALID_FILE_NAME = "WARNINGSXAPI_INVALID_FILE_NAME"
    WARNINGS_CSV_INVALID_FILE_FORMAT = "WARNINGS_CSV_INVALID_FILE_FORMAT"
    WARNINGS_CSV_LINE_CORRUPTED = "WARNINGS_CSV_LINE_CORRUPTED"
    WARNINGS_WRONG_CSV_FILE_REQUIRED_COLUMNS_NOT_FOUND = "WARNINGS_WRONG_CSV_FILE_REQUIRED_COLUMNS_NOT_FOUND"
    WARNINGS_CSV_IMPORT_LIMIT_REACHED = "WARNINGS_CSV_IMPORT_LIMIT_REACHED"
    WARNINGS_WRONG_CSV_FILE_REQUIRED_HEADER_NOT_FOUND = "WARNINGS_WRONG_CSV_FILE_REQUIRED_HEADER_NOT_FOUND"
    WARNINGSXAPI_FILE_IS_TOO_LARGE = "WARNINGSXAPI_FILE_IS_TOO_LARGE"
    WARNINGSXAPI_SBC_CERT_FQDN_MISMATCH = "WARNINGSXAPI_SBC_CERT_FQDN_MISMATCH"
    WARNINGSXAPI_SBC_CERT_EXPIRED = "WARNINGSXAPI_SBC_CERT_EXPIRED"
    WARNINGSXAPI_SBC_KEY_CERT_MISMATCH = "WARNINGSXAPI_SBC_KEY_CERT_MISMATCH"
    WARNINGSXAPI_NON_EXISTENT_EXT_NUMBER = "WARNINGSXAPI_NON_EXISTENT_EXT_NUMBER"
    WARNINGSXAPI_MCM_MODE_REQUIRED = "WARNINGSXAPI_MCM_MODE_REQUIRED"
    WARNINGS_INTERNATIONALPREFIX_IS_MISSING = "WARNINGS_INTERNATIONALPREFIX_IS_MISSING"
    WARNINGS_TIMEZONEID_IS_MISSING = "WARNINGS_TIMEZONEID_IS_MISSING"
    WARNINGSXAPI_CHAT_LOG_IS_DISABLED = "WARNINGSXAPI_CHAT_LOG_IS_DISABLED"
    WARNINGS_WAKEUP_IVR_EXISTS = "WARNINGS_WAKEUP_IVR_EXISTS"
    WARNINGS_RING_GROUP_ENABLE_PAGING = "WARNINGS_RING_GROUP_ENABLE_PAGING"
    WARNINGSXAPI_CREATE_1_SIP_TRUCK_EMERGENCY = "WARNINGSXAPI_CREATE_1_SIP_TRUCK_EMERGENCY"
    WARNINGS_DELETING_ALREADY_IN_PROGRESS = "WARNINGS_DELETING_ALREADY_IN_PROGRESS"
    WARNINGS_INVALID_IP_MASK = "WARNINGS_INVALID_IP_MASK"
    WARNINGS_TOO_MANY_BACKUPS = "WARNINGS_TOO_MANY_BACKUPS"
    WARNINGS_BACKUP_LOCATION_CONFIG_ERROR = "WARNINGS_BACKUP_LOCATION_CONFIG_ERROR"
    WARNINGS_BACKUP_NOT_FOUND_OR_INVALID = "WARNINGS_BACKUP_NOT_FOUND_OR_INVALID"
    WARNINGS_INVALID_CALL_FLOW_FILE = "WARNINGS_INVALID_CALL_FLOW_FILE"
    WARNINGS_ALREADY_EXPIRED = "WARNINGS_ALREADY_EXPIRED"
    WARNINGS_CALL_FLOW_MUST_BE_ALPHANUMERIC = "WARNINGS_CALL_FLOW_MUST_BE_ALPHANUMERIC"
    WARNINGS_EXTRACTING_OUTSIDE_THE_DESTINATION_DIRECTORY = "WARNINGS_EXTRACTING_OUTSIDE_THE_DESTINATION_DIRECTORY"
    WARNINGS_INVALID_EXTENSION_NUMBER_LENGTH = "WARNINGS_INVALID_EXTENSION_NUMBER_LENGTH"
    WARNINGS_DN_NUMBER_CANNOT_BE_USED = "WARNINGS_DN_NUMBER_CANNOT_BE_USED"
    WARNINGS_WIRESHARK_NOT_FOUND = "WARNINGS_WIRESHARK_NOT_FOUND"
    WARNINGS_CAPTURE_LOCALHOST_NOT_ALLOWED = "WARNINGS_CAPTURE_LOCALHOST_NOT_ALLOWED"
    WARNINGS_CAPTURE_ONGOING = "WARNINGS_CAPTURE_ONGOING"
    WARNINGS_CANNOT_DELETE_TRUNKS_BINDED_ERMERGENCY_NUMBER = "WARNINGS_CANNOT_DELETE_TRUNKS_BINDED_ERMERGENCY_NUMBER"
    WARNINGS_BLACKLIST_NUMBER_LIMIT_EXCEEDED = "WARNINGS_BLACKLIST_NUMBER_LIMIT_EXCEEDED"
    WARNINGS_DOUBLE_QUOTES_NOT_ALLOWED = "WARNINGS_DOUBLE_QUOTES_NOT_ALLOWED"
    WARNINGS_MCU_REQUEST_ALREADY_IN_PROGRESS = "WARNINGS_MCU_REQUEST_ALREADY_IN_PROGRESS"
    WARNINGS_MCU_LIMIT_REACHED = "WARNINGS_MCU_LIMIT_REACHED"
    WARNINGS_MCU_WEBMEETING_BRIDGE_NOT_FOUND = "WARNINGS_MCU_WEBMEETING_BRIDGE_NOT_FOUND"
    WARNINGS_MCU_REQUEST_NOT_FOUND = "WARNINGS_MCU_REQUEST_NOT_FOUND"
    WARNINGS_MCU_REQUEST_TIMEOUT = "WARNINGS_MCU_REQUEST_TIMEOUT"
    WARNINGS_SUPPORTED_MEDIA_FORMAT_WAV = "WARNINGS_SUPPORTED_MEDIA_FORMAT_WAV"
    WARNINGS_NO_SECRET_DEFINED = "WARNINGS_NO_SECRET_DEFINED"
    WARNINGS_INVALID_SECURITY_CODE = "WARNINGS_INVALID_SECURITY_CODE"
    WARNINGS_UNABLE_REACH_UPDATES_SERVER = "WARNINGS_UNABLE_REACH_UPDATES_SERVER"
    WARNINGS_ERROR_DOWNLOADING_FROM_UPDATES_SERVER = "WARNINGS_ERROR_DOWNLOADING_FROM_UPDATES_SERVER"
