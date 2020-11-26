from sqlalchemy.orm import Session

from .query import SangrealQuery


class SangrealSession(Session):
    def __init__(self,
                 bind=None,
                 autoflush=True,
                 expire_on_commit=True,
                 _enable_transaction_accounting=True,
                 autocommit=False,
                 twophase=False,
                 weak_identity_map=True,
                 binds=None,
                 extension=None,
                 enable_baked_queries=True,
                 info=None,
                 query_cls=SangrealQuery):
        super().__init__(
            bind=bind,
            autoflush=autoflush,
            expire_on_commit=expire_on_commit,
            _enable_transaction_accounting=_enable_transaction_accounting,
            autocommit=autocommit,
            twophase=twophase,
            weak_identity_map=weak_identity_map,
            binds=binds,
            extension=extension,
            enable_baked_queries=enable_baked_queries,
            info=info,
            query_cls=query_cls)
