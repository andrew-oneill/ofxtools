# coding: utf-8
"""
Data structures for bank download - OFX Section 11
"""
# local imports
from ofxtools.Types import String, NagString, Decimal, Integer, OneOf, DateTime, Bool
from ofxtools.models.base import Aggregate, List, TranList, SubAggregate, Unsupported
from ofxtools.models.common import STATUS, MSGSETCORE, SVCSTATUSES
from ofxtools.models.i18n import (
    CURRENCY,
    ORIGCURRENCY,
    Origcurrency,
    CURRENCY_CODES,
    COUNTRY_CODES,
)


__all__ = [
    "BANKACCTFROM",
    "CCACCTFROM",
    "BANKACCTTO",
    "CCACCTTO",
    "BANKACCTINFO",
    "CCACCTINFO",
    "INCTRAN",
    "PAYEE",
    "EMAILPROF",
    "LEDGERBAL",
    "AVAILBAL",
    "BALLIST",
    "STMTTRN",
    "BANKTRANLIST",
    "STMTRQ",
    "STMTRS",
    "STMTTRNRQ",
    "STMTTRNRS",
    "CLOSING",
    "STMTENDRQ",
    "STMTENDRS",
    "STMTENDTRNRQ",
    "STMTENDTRNRS",
    "BANKMSGSRQV1",
    "BANKMSGSRSV1",
    "BANKMSGSETV1",
    "BANKMSGSET",
    "EMAILPROF",
]


# Enums used in aggregate validation
INV401KSOURCES = (
    "PRETAX",
    "AFTERTAX",
    "MATCH",
    "PROFITSHARING",
    "ROLLOVER",
    "OTHERVEST",
    "OTHERNONVEST",
)
# OFX section 11.3.1.1
ACCTTYPES = ("CHECKING", "SAVINGS", "MONEYMRKT", "CREDITLINE", "CD")
TRNTYPES = (
    "CREDIT",
    "DEBIT",
    "INT",
    "DIV",
    "FEE",
    "SRVCHG",
    "DEP",
    "ATM",
    "POS",
    "XFER",
    "CHECK",
    "PAYMENT",
    "CASH",
    "DIRECTDEP",
    "DIRECTDEBIT",
    "REPEATPMT",
    "OTHER",
)


class BANKACCTFROM(Aggregate):
    """ OFX section 11.3.1 """

    bankid = String(9, required=True)
    branchid = String(22)
    acctid = String(22, required=True)
    accttype = OneOf(*ACCTTYPES, required=True)
    acctkey = String(22)


class BANKACCTTO(Aggregate):
    """ OFX section 11.3.1 """

    bankid = String(9, required=True)
    branchid = String(22)
    acctid = String(22, required=True)
    accttype = OneOf(*ACCTTYPES, required=True)
    acctkey = String(22)


class CCACCTFROM(Aggregate):
    """ OFX section 11.3.2 """

    acctid = String(22, required=True)
    acctkey = String(22)


class CCACCTTO(Aggregate):
    """ OFX section 11.3.2 """

    acctid = String(22, required=True)
    acctkey = String(22)


class BANKACCTINFO(Aggregate):
    """ OFX section 11.3.3 """

    bankacctfrom = SubAggregate(BANKACCTFROM, required=True)
    suptxdl = Bool(required=True)
    xfersrc = Bool(required=True)
    xferdest = Bool(required=True)
    svcstatus = OneOf(*SVCSTATUSES, required=True)


class CCACCTINFO(Aggregate):
    """ OFX section 11.3.4 """

    ccacctfrom = SubAggregate(CCACCTFROM, required=True)
    suptxdl = Bool(required=True)
    xfersrc = Bool(required=True)
    xferdest = Bool(required=True)
    svcstatus = OneOf(*SVCSTATUSES, required=True)


class INCTRAN(Aggregate):
    """ OFX section 11.4.2.1 """

    dtstart = DateTime()
    dtend = DateTime()
    include = Bool(required=True)


class STMTRQ(Aggregate):
    """ OFX section 11.4.2.1 """

    bankacctfrom = SubAggregate(BANKACCTFROM, required=True)
    inctran = SubAggregate(INCTRAN)
    includepending = Bool()
    inctranimg = Bool()


class PAYEE(Aggregate):
    """ OFX section 12.5.2.1 """

    name = NagString(32, required=True)
    addr1 = String(32, required=True)
    addr2 = String(32)
    addr3 = String(32)
    city = String(32, required=True)
    state = String(5, required=True)
    postalcode = String(11, required=True)
    country = OneOf(*COUNTRY_CODES)
    phone = String(32, required=True)


class STMTTRN(Aggregate, Origcurrency):
    """ OFX section 11.4.3 """

    trntype = OneOf(*TRNTYPES, required=True)
    dtposted = DateTime(required=True)
    dtuser = DateTime()
    dtavail = DateTime()
    trnamt = Decimal(required=True)
    fitid = String(255, required=True)
    correctfitid = String(255)
    correctaction = OneOf("REPLACE", "DELETE")
    srvrtid = String(10)
    checknum = String(12)
    refnum = String(32)
    sic = Integer()
    payeeid = String(12)
    name = String(32)
    payee = SubAggregate(PAYEE)
    extdname = String(100)
    bankacctto = SubAggregate(BANKACCTTO)
    ccacctto = SubAggregate(CCACCTTO)
    memo = String(255)
    imagedata = Unsupported()
    currency = SubAggregate(CURRENCY)
    origcurrency = SubAggregate(ORIGCURRENCY)
    inv401ksource = OneOf(*INV401KSOURCES)

    optionalMutexes = [
        ("ccacctto", "bankacctto"),
        ("name", "payee"),
        ("currency", "origcurrency"),
    ]


class BANKTRANLIST(TranList):
    """ OFX section 11.4.2.2 """

    dataTags = ["STMTTRN"]


class LEDGERBAL(Aggregate):
    """ OFX section 11.4.2.2 """

    balamt = Decimal(required=True)
    dtasof = DateTime(required=True)


class AVAILBAL(Aggregate):
    """ OFX section 11.4.2.2 """

    balamt = Decimal(required=True)
    dtasof = DateTime(required=True)


class BALLIST(List):
    """ OFX section 11.4.2.2 & 13.9.2.7 """

    dataTags = ["BAL"]


class STMTRS(Aggregate):
    """ OFX section 11.4.2.2 """

    curdef = OneOf(*CURRENCY_CODES, required=True)
    bankacctfrom = SubAggregate(BANKACCTFROM, required=True)
    banktranlist = SubAggregate(BANKTRANLIST)
    banktranlistp = Unsupported()
    ledgerbal = SubAggregate(LEDGERBAL, required=True)
    availbal = SubAggregate(AVAILBAL)
    cashadvbalamt = Decimal()
    intrate = Decimal()
    ballist = SubAggregate(BALLIST)
    mktginfo = String(360)

    @property
    def account(self):
        return self.bankacctfrom

    @property
    def transactions(self):
        return self.banktranlist

    @property
    def balance(self):
        return self.ledgerbal


class STMTTRNRQ(Aggregate):
    """ OFX section 11.4.2.1 """

    trnuid = String(36, required=True)
    stmtrq = SubAggregate(STMTRQ)


class STMTTRNRS(Aggregate):
    """ OFX section 11.4.2.2 """

    trnuid = String(36, required=True)
    status = SubAggregate(STATUS, required=True)
    stmtrs = SubAggregate(STMTRS)

    @property
    def statement(self):
        return self.stmtrs


class CLOSING(Aggregate, Origcurrency):
    """ OFX section 11.5.2 """
    fitid = String(255, required=True)
    dtopen = DateTime()
    dtclose = DateTime(required=True)
    dtnext = DateTime()
    balopen = Decimal()
    balclose = Decimal(required=True)
    balmin = Decimal()
    depandcredit = Decimal()
    chkanddebit = Decimal()
    totalfees = Decimal()
    totalint = Decimal()
    dtpoststart = DateTime(required=True)
    dtpostend = DateTime(required=True)
    mktginfo = String(360)
    currency = SubAggregate(CURRENCY)
    origcurrency = SubAggregate(ORIGCURRENCY)


class STMTENDRQ(Aggregate):
    """ OFX section 11.5.1 """
    bankacctfrom = SubAggregate(BANKACCTFROM, required=True)
    dtstart = DateTime()
    dtend = DateTime()


class STMTENDRS(List):
    """ OFX section 11.5.2 """
    curdef = OneOf(*CURRENCY_CODES, required=True)
    bankacctfrom = SubAggregate(BANKACCTFROM, required=True)

    metadataTags = ["CURDEF", "BANKACCTFROM"]
    dataTags = ["CLOSING"]

    def __init__(self, curdef, bankacctfrom, *members):
        self.curdef = curdef
        self.bankacctfrom = bankacctfrom
        super().__init__(*members)


class STMTENDTRNRQ(Aggregate):
    """ OFX section 11.5.1 """

    trnuid = String(36, required=True)
    stmtendrq = SubAggregate(STMTENDRQ)


class STMTENDTRNRS(Aggregate):
    """ OFX section 11.5.2 """

    trnuid = String(36, required=True)
    status = SubAggregate(STATUS, required=True)
    stmtendrs = SubAggregate(STMTENDRS)

    @property
    def statement(self):
        return self.stmtendrs


class BANKMSGSRQV1(List):
    """ OFX section 11.13.1.1.1 """

    dataTags = ["STMTTRNRQ", "STMTENDRQ", "STPCHKTRNRQ", "INTRATRNRQ", "RECINTRATRNRQ", "BANKMAILTRNRQ", "STPCHKSYNCRQ", "INTRASYNCRQ", "RECINTRASYNCRQ", "BANKMAILSYNCRQ"]


class BANKMSGSRSV1(List):
    """ OFX section 11.13.1.1.2 """

    dataTags = ["STMTTRNRS", "STMTENDRS", "STPCHKTRNRS", "INTRATRNRS", "RECINTRATRNRS", "BANKMAILTRNRS", "STPCHKSYNCRS", "INTRASYNCRS", "RECINTRASYNCRS", "BANKMAILSYNCRS"]

    @property
    def statements(self):
        return [trnrs.statement for trnrs in self]


class EMAILPROF(Aggregate):
    """ OFX section 11.13.2.4 """

    canemail = Bool(required=True)
    cannotify = Bool(required=True)


class BANKMSGSETV1(Aggregate):
    """ OFX section 11.13.2.1 """

    msgsetcore = SubAggregate(MSGSETCORE, required=True)
    invalidaccttype = OneOf(*ACCTTYPES)
    closingavail = Bool(required=True)
    pendingavail = Bool()
    xferprof = Unsupported()
    stopchkprof = Unsupported()
    emailprof = SubAggregate(EMAILPROF, required=True)
    imageprof = Unsupported()


class BANKMSGSET(Aggregate):
    """ OFX section 7.3 """

    bankmsgsetv1 = SubAggregate(BANKMSGSETV1, required=True)
