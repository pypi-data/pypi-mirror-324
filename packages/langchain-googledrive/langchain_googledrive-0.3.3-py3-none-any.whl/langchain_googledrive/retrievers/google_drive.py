from typing import Any, Dict, List, Literal

from langchain_core.callbacks.manager import (
    AsyncCallbackManagerForRetrieverRun,
    CallbackManagerForRetrieverRun,
)
from langchain_core.documents import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import (
    ConfigDict,
    model_validator,
)

from ..utilities.google_drive import (
    GoogleDriveUtilities,
    get_template,
)


class GoogleDriveRetriever(GoogleDriveUtilities, BaseRetriever):
    """Wrapper around Google Drive API.

    The application must be authenticated with a json file.
    The format may be for a user or for an application via a service account.
    The environment variable `GOOGLE_ACCOUNT_FILE` may be set to reference this file.
    For more information, see [here]
    (https://developers.google.com/workspace/guides/auth-overview).
    """

    model_config = ConfigDict(
        extra="allow",
        frozen=False,
    )

    mode: Literal[
        "snippets", "snippets-markdown", "documents", "documents-markdown"
    ] = "snippets-markdown"

    @model_validator(mode="before")
    @classmethod
    def validate_template(
        cls,
        v: Dict[str, Any],
    ) -> Dict[str, Any]:
        folder_id = v.get("folder_id")

        if not v.get("template"):
            if folder_id:
                template = get_template("gdrive-query-in-folder")
            else:
                template = get_template("gdrive-query")
            v["template"] = template
        return v

    def _get_relevant_documents(
        self, query: str, *, run_manager: CallbackManagerForRetrieverRun
    ) -> List[Document]:
        """Get documents relevant for a query.

        Args:
            query: string to find relevant documents for

        Returns:
            List of relevant documents
        """
        return list(
            self.lazy_get_relevant_documents(
                query=query,
                run_manager=run_manager,
            )
        )

    async def _aget_relevant_documents(
        self, query: str, *, run_manager: AsyncCallbackManagerForRetrieverRun
    ) -> List[Document]:
        raise NotImplementedError("GoogleSearchRun does not support async")
