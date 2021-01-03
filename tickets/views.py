import os
import json
import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render


BASE_DIR = os.path.dirname(os.path.realpath(__file__))
DB = os.path.join(BASE_DIR, 'db.json')


class Tickets(APIView):

    def initDB(self):
        if not os.path.exists(DB):
            f = open(DB, "w")
            f.write("{}")
            f.close()

    def get(self, request):
        try:
            self.initDB()
            f = open(DB, "rt")
            data = f.read()
            dataJson = json.loads(data)

            f.close()

            response_data = {
                "success": True,
                "message": "All tickets",
                "data": dataJson
            }
            return Response(response_data, status=status.HTTP_200_OK)

        except:
            response_data = {
                "success": False,
                "message": "Something went wrong"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            ticketInfo = request.data

            # print(ticketInfo)

            ticketNo = ticketInfo.ticketNo
            noOfPeople = ticketInfo.noOfPeople
            amount = ticketInfo.amount

            validFor = 0

            # print(ticketInfo.validFor)

            if ticketInfo.validFor:
                # print("--------")
                validFor = ticketInfo.validFor

            self.initDB()

            f = open(DB, "rt")
            data = f.read()
            dataJson = json.loads(data)

            if ticketNo in dataJson:
                f.close()
                response_data = {
                    "success": False,
                    "message": "Ticket already exists"
                }
                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            dataJson[ticketNo] = {
                "ticketNo": ticketNo,
                "noOfPeople": noOfPeople,
                "amount": amount,
            }

            now = datetime.datetime.now()

            expiryDateTimestamp = now.timestamp() + validFor

            if validFor != 0:
                dataJson[ticketNo]["expiryDate"] = expiryDateTimestamp

            # convert data into json
            dataJsonToString = json.dumps(dataJson)
            data = data.replace(data, dataJsonToString)
            f.close()

            f = open(DB, "wt")
            f.write(data)
            f.close()

            response_data = {
                "success": True,
                "message": "Ticket " + ticketNo + " has been created successfully",
                "data": dataJson
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except:

            response_data = {
                "success": False,
                "message": "Something went wrong"
            }
            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)


class Ticket(APIView):
    def initDB(self):
        if not os.path.exists(DB):
            f = open(DB, "w")
            f.write("{}")
            f.close()

    def get(self, request, ticketNo):
        try:
            self.initDB()

            f = open(DB, "rt")

            data = f.read()
            dataJson = json.loads(data)

            # check if ticket available or not
            if ticketNo not in dataJson:
                f.close()
                response_data = {
                    "success": False,
                    "message": "Ticket doesn't exist"
                }

                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            # check expiry date
            nowTimestamp = datetime.datetime.now().timestamp()

            if "expiryDate" in dataJson[ticketNo] and nowTimestamp > dataJson[ticketNo]["expiryDate"]:
                f.close()
                response_data = {
                    "success": False,
                    "message": "Ticket has been expired",
                    "type": "expired"
                }

                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            f.close()
            response_data = {
                "success": True,
                "message": "Ticket Exist",
                "data": dataJson[ticketNo]
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except:
            response_data = {
                "success": False,
                "message": "Something went wrong"
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, ticketNo):
        try:
            self.initDB()

            f = open(DB, "rt")

            data = f.read()
            dataJson = json.loads(data)

            # check if ticket available or not
            if ticketNo not in dataJson:
                f.close()
                response_data = {
                    "success": False,
                    "message": "Ticket doesn't exist"
                }

                return Response(response_data, status=status.HTTP_404_NOT_FOUND)

            # check expiry date
            nowTimestamp = datetime.datetime.now().timestamp()

            if "expiryDate" in dataJson[ticketNo] and nowTimestamp > dataJson[ticketNo]["expiryDate"]:
                f.close()
                response_data = {
                    "success": False,
                    "message": "Ticket has been expired",
                    "type": "expired"
                }

                return Response(response_data, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

            ticketData = dataJson[ticketNo]

            dataJson.pop(ticketNo)

            data = data.replace(data, json.dumps(dataJson))
            f.close()

            f = open(DB, "wt")
            f.write(data)
            f.close()

            response_data = {
                "success": True,
                "message": "Ticket has been deleted successfully",
                "data": ticketData
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except:
            response_data = {
                "success": False,
                "message": "Something went wrong"
            }

            return Response(response_data, status=status.HTTP_400_BAD_REQUEST)
            