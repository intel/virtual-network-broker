RTE_TARGET ?= x86_64-native-linuxapp-gcc

include $(RTE_SDK)/mk/rte.vars.mk

APP = SecMonAgent
SRCS-y := SecMonAgent.c
CFLAGS += -O3 -g -Wall 
CFLAGS += $(WERROR_FLAGS)
LDFLAGS += -L/home/aricent/plugins

include $(RTE_SDK)/mk/rte.extapp.mk
