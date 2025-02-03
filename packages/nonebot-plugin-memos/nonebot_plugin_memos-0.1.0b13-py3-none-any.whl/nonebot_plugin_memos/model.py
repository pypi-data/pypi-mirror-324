from pydantic import BaseModel, Field
from typing import Literal


ListNodeKind = Literal["KIND_UNSPECIFIED", "ORDERED", "UNORDERED", "DESCRIPTION"]
ListNodeKindDefault = "KIND_UNSPECIFIED"

UserRole = Literal["ROLE_UNSPECIFIED", "HOST", "ADMIN", "USER"]
UserRoleDefault = "ROLE_UNSPECIFIED"


IdentityProviderType = Literal["TYPE_UNSPECIFIED", "OAUTH2"]
IdentityProviderTypeDefault = "TYPE_UNSPECIFIED"

WorkspaceStorageSettingStorageType = Literal["STORAGE_TYPE_UNSPECIFIED", "DATABASE", "LOCAL", "S3"]
WorkspaceStorageSettingStorageTypeDefault = "STORAGE_TYPE_UNSPECIFIED"


InboxStatus = Literal["STATUS_UNSPECIFIED", "UNREAD", "ARCHIVED"]
InboxStatusDefault = "STATUS_UNSPECIFIED"

InboxType = Literal["TYPE_UNSPECIFIED", "MEMO_COMMENT", "VERSION_UPDATE"]
InboxTypeDefault = "TYPE_UNSPECIFIED"

MemoRelationType = Literal["TYPE_UNSPECIFIED", "REFERENCE", "COMMENT"]
MemoRelationTypeDefault = "TYPE_UNSPECIFIED"

NodeType = Literal[
    "NODE_UNSPECIFIED",
    "LINE_BREAK",
    "PARAGRAPH",
    "CODE_BLOCK",
    "HEADING",
    "HORIZONTAL_RULE",
    "BLOCKQUOTE",
    "LIST",
    "ORDERED_LIST_ITEM",
    "UNORDERED_LIST_ITEM",
    "TASK_LIST_ITEM",
    "MATH_BLOCK",
    "TABLE",
    "EMBEDDED_CONTENT",
    "TEXT",
    "BOLD",
    "ITALIC",
    "BOLD_ITALIC",
    "CODE",
    "IMAGE",
    "LINK",
    "AUTO_LINK",
    "TAG",
    "STRIKETHROUGH",
    "ESCAPING_CHARACTER",
    "MATH",
    "HIGHLIGHT",
    "SUBSCRIPT",
    "SUPERSCRIPT",
    "REFERENCED_CONTENT",
    "SPOILER",
    "HTML_ELEMENT",
]
NodeTypeDefault = "NODE_UNSPECIFIED"

ReactionType = Literal[
    "TYPE_UNSPECIFIED",
    "THUMBS_UP",
    "THUMBS_DOWN",
    "HEART",
    "FIRE",
    "CLAPPING_HANDS",
    "LAUGH",
    "OK_HAND",
    "ROCKET",
    "EYES",
    "THINKING_FACE",
    "CLOWN_FACE",
    "QUESTION_MARK",
]
ReactionTypeDefault = "TYPE_UNSPECIFIED"

RowStatus = Literal["ROW_STATUS_UNSPECIFIED", "ACTIVE", "ARCHIVED"]
RowStatusDefault = "ROW_STATUS_UNSPECIFIED"

Visibility = Literal["VISIBILITY_UNSPECIFIED", "PRIVATE", "PROTECTED", "PUBLIC"]
VisibilityDefault = "VISIBILITY_UNSPECIFIED"


class MemoservicerenameMemotagbody(BaseModel):
    oldTag: str
    newTag: str


class SimpleMemo(BaseModel):
    name: str
    uid: str
    snippet: str


class MemoRelation(BaseModel):
    memo: SimpleMemo
    relatedMemo: SimpleMemo
    type: MemoRelationType = Field(MemoRelationTypeDefault)


class MemoservicesetMemorelationsbody(BaseModel):
    relations: list[MemoRelation]


class Memoproperty(BaseModel):
    tags: list[str]
    hasLink: bool
    hasTaskList: bool
    hasCode: bool
    hasIncompleteTasks: bool


class Memopropertyentity(BaseModel):
    name: str
    property: Memoproperty
    displayTime: str


class Resource(BaseModel):
    name: str
    uid: str
    createTime: str
    filename: str
    content: str
    externalLink: str
    type: str
    size: str
    memo: str


class MemoservicesetMemoResourcesbody(BaseModel):
    resources: list[Resource]


class Reaction(BaseModel):
    id: int
    creator: str
    contentId: str
    reactionType: ReactionType = Field(ReactionTypeDefault)


class MemoserviceupsertMemoReactionbody(BaseModel):
    reaction: Reaction


class Memo(BaseModel):
    name: str
    uid: str
    rowStatus: RowStatus = Field(RowStatusDefault)
    creator: str
    createTime: str
    updateTime: str
    displayTime: str
    content: str

    visibility: Visibility = Field(VisibilityDefault)
    tags: list[str]
    pinned: bool
    resources: list[Resource]
    relations: list[MemoRelation]
    reactions: list[Reaction]
    property: Memoproperty
    parent: str | None = Field(None)
    snippet: str


class UserservicecreateUseraccesstokenbody(BaseModel):
    description: str
    expiresAt: str


class Workspacestoragesettings3config(BaseModel):
    accessKeyId: str
    accessKeySecret: str
    endpoint: str
    region: str
    bucket: str


class ActivityMemocommentpayload(BaseModel):
    memoId: int
    relatedMemoId: int


class Activityversionupdatepayload(BaseModel):
    version: str


class Activitypayload(BaseModel):
    memoComment: ActivityMemocommentpayload
    versionUpdate: Activityversionupdatepayload


class Fieldmapping(BaseModel):
    identifier: str
    displayName: str
    email: str


class Oauth2config(BaseModel):
    clientId: str
    clientSecret: str
    authUrl: str
    tokenUrl: str
    userInfoUrl: str
    scopes: list[str]
    fieldMapping: Fieldmapping


class Identityproviderconfig(BaseModel):
    oauth2Config: Oauth2config


class Identityprovider(BaseModel):
    name: str
    type: IdentityProviderType = Field(IdentityProviderTypeDefault)
    title: str
    identifierFilter: str
    config: Identityproviderconfig


class Usersetting(BaseModel):
    name: str
    locale: str
    appearance: str
    memoVisibility: str


class Workspacecustomprofile(BaseModel):
    title: str
    description: str
    logoUrl: str
    locale: str
    appearance: str


class Workspacegeneralsetting(BaseModel):
    disallowUserRegistration: bool
    disallowPasswordAuth: bool
    additionalScript: str
    additionalStyle: str
    customProfile: Workspacecustomprofile
    weekStartDayOffset: int
    disallowChangeUsername: bool
    disallowChangeNickname: bool


class WorkspaceMemorelatedsetting(BaseModel):
    disallowPublicVisibility: bool
    displayWithUpdateTime: bool
    contentLengthLimit: int
    enableAutoCompact: bool
    enableDoubleClickEdit: bool
    enableLinkPreview: bool
    enableComment: bool


class Workspacestoragesetting(BaseModel):
    storageType: WorkspaceStorageSettingStorageType = Field(WorkspaceStorageSettingStorageTypeDefault)
    filepathTemplate: str
    uploadSizeLimitMb: str
    s3Config: Workspacestoragesettings3config


class Workspacesetting(BaseModel):
    name: str
    generalSetting: Workspacegeneralsetting
    storageSetting: Workspacestoragesetting
    memoRelatedSetting: WorkspaceMemorelatedsetting


class Protobufany(BaseModel):
    type: str = Field(..., alias="@type")


class Apihttpbody(BaseModel):
    contentType: str
    data: str
    extensions: list[Protobufany]


class Googlerpcstatus(BaseModel):
    code: int
    message: str
    details: list[Protobufany]


class Activity(BaseModel):
    name: str
    creatorId: int
    type: str
    level: str
    createTime: str
    payload: Activitypayload


class AutoLinkNode(BaseModel):
    url: str
    isRawText: bool


class BoldItalicNode(BaseModel):
    symbol: str
    content: str


class CodeblockNode(BaseModel):
    language: str
    content: str


class CodeNode(BaseModel):
    content: str


class CreateMemorequest(BaseModel):
    content: str
    visibility: Visibility = Field(VisibilityDefault)
    resources: list[Resource]
    relations: list[MemoRelation]


class CreateWebhookrequest(BaseModel):
    name: str
    url: str


class EmbeddedcontentNode(BaseModel):
    resourceName: str
    params: str


class EscapingcharacterNode(BaseModel):
    symbol: str


class HtmlelementNode(BaseModel):
    tagName: str
    attributes: dict


class HighlightNode(BaseModel):
    content: str


class HorizontalruleNode(BaseModel):
    symbol: str


class ImageNode(BaseModel):
    altText: str
    url: str


class Inbox(BaseModel):
    name: str
    sender: str
    receiver: str
    status: InboxStatus = Field(InboxStatusDefault)
    createTime: str
    type: InboxType = Field(InboxTypeDefault)
    activityId: int


class ItalicNode(BaseModel):
    symbol: str
    content: str


class Linkmetadata(BaseModel):
    title: str
    description: str
    image: str


class LinkNode(BaseModel):
    text: str
    url: str


class Listidentityprovidersresponse(BaseModel):
    identityProviders: list[Identityprovider]


class Listinboxesresponse(BaseModel):
    inboxes: list[Inbox]


class Listmemocommentsresponse(BaseModel):
    memos: list[Memo]


class Listmemopropertiesresponse(BaseModel):
    entities: list[Memopropertyentity]


class Listmemoreactionsresponse(BaseModel):
    reactions: list[Reaction]


class Listmemorelationsresponse(BaseModel):
    relations: list[MemoRelation]


class Listmemoresourcesresponse(BaseModel):
    resources: list[Resource]


class Listmemotagsresponse(BaseModel):
    tagAmounts: dict


class Listmemosresponse(BaseModel):
    memos: list[Memo]
    nextPageToken: str


class Listresourcesresponse(BaseModel):
    resources: list[Resource]


class Useraccesstoken(BaseModel):
    accessToken: str
    description: str
    issuedAt: str
    expiresAt: str


class Listuseraccesstokensresponse(BaseModel):
    accessTokens: list[Useraccesstoken]


class User(BaseModel):
    id: int
    role: UserRole = Field(UserRoleDefault)
    username: str
    email: str
    nickname: str
    avatarUrl: str
    description: str
    password: str
    rowStatus: RowStatus = Field(RowStatusDefault)
    createTime: str
    updateTime: str


class ListUsersresponse(BaseModel):
    users: list[User]


class MathblockNode(BaseModel):
    content: str


class MathNode(BaseModel):
    content: str


class TextNode(BaseModel):
    content: str


class TagNode(BaseModel):
    content: str


class StrikethroughNode(BaseModel):
    content: str


class SubscriptNode(BaseModel):
    content: str


class SuperscriptNode(BaseModel):
    content: str


class ReferencedcontentNode(BaseModel):
    resourceName: str
    params: str


class SpoilerNode(BaseModel):
    content: str


class Parsemarkdownrequest(BaseModel):
    markdown: str


class RestoremarkdownNodesresponse(BaseModel):
    markdown: str


class Searchusersresponse(BaseModel):
    users: list[User]


class StringifymarkdownNodesresponse(BaseModel):
    plainText: str


class Webhook(BaseModel):
    id: int
    creatorId: int
    createTime: str
    updateTime: str
    rowStatus: RowStatus = Field(RowStatusDefault)
    name: str
    url: str


class Listwebhooksresponse(BaseModel):
    webhooks: list[Webhook]


class Workspaceprofile(BaseModel):
    owner: str
    version: str
    mode: str
    instanceUrl: str


class Setting(BaseModel):
    generalSetting: Workspacegeneralsetting
    storageSetting: Workspacestoragesetting
    memoRelatedSetting: WorkspaceMemorelatedsetting
